import csv
import gzip
import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from pipeline.construire_base import VARIABLES_METEO, build_database, department


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        # Un répertoire du projet évite les répertoires TEMP isolés non
        # accessibles dans certains environnements Windows.
        base = Path(__file__).resolve().parents[1]
        self.temp = tempfile.TemporaryDirectory(prefix='.sqlite-tests-', dir=base)
        self.root = Path(self.temp.name).resolve()
        if not self.root.is_relative_to(base.resolve()):
            raise ValueError('Répertoire temporaire hors du projet')
        self.addCleanup(self.temp.cleanup)
        self.data = self.root / 'data'
        self.data.mkdir()
        (self.data / 'meteo_quotidienne').mkdir()
        self.output = self.root / 'test.sqlite'
        self.fire_header = ['Année', 'Numéro', 'Département', 'Code INSEE', 'Nom de la commune',
                            'Date de première alerte', 'Surface parcourue (m2)', 'Surface forêt (m2)',
                            'Nature', 'Précision des surfaces', 'Précision de la donnée',
                            'Décès ou bâtiments touchés', 'Nombre de décès',
                            'Nombre de bâtiments totalement détruits', 'Nombre de bâtiments partiellement détruits']
        self.fires = [['2025', '12', '33', '33099', 'Ancien libellé', '2025-06-01 16:00:00',
                       '10000', '5000', '', '', '', 'Non', '', '', '']]
        self.write('communes_na.csv', ['code_insee', 'commune', 'departement', 'lat', 'lon', 'surface_ha', 'population'],
                   [['33001', 'Commune de référence', '33', '44.8', '-0.5', '100', '500']], ',')
        self.write_fires()
        self.write('meteo_foret_na.csv', ['date', 'num_dep', 'niveau_j1', 'niveau_j2', 'nom_dep', 'dep_nom'],
                   [['2025-06-01T23:30:00Z', '33', '2', '3', '', 'Gironde']], ';')
        self.write('meteo_quotidienne/33.csv', ['date', 'departement', *VARIABLES_METEO],
                   [['2025-06-01', '33', '0', '-2', '0', '5', '7', '80', '1', '0.2']], ',')

    def write(self, name, header, rows, delimiter, preamble=()):
        with (self.data / name).open('w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            for line in preamble:
                writer.writerow([line])
            writer.writerow(header)
            writer.writerows(rows)

    def write_fires(self):
        self.write('incendies.csv', self.fire_header, self.fires, ';', ['Nombre : 1', 'Sélection Gironde'])

    def connect(self):
        con = sqlite3.connect(self.output)
        con.execute('PRAGMA foreign_keys=ON')
        self.addCleanup(con.close)
        return con

    def build(self, replace=False):
        return build_database(self.data, self.output, replace=replace)

    def test_import_lineage_missing_values_and_centre_are_not_fire_coordinates(self):
        report = self.build()
        con = self.connect()
        self.assertEqual(report['tables']['fait_incendie'], 1)
        self.assertEqual(con.execute('SELECT cause,nombre_deces,consequence_signalee,surface_parcourue_ha,ligne_csv FROM v_incendies_detail').fetchone(),
                         (None, None, 0, 1.0, 4))
        self.assertEqual(con.execute("SELECT latitude_centre,statut_reference FROM dim_commune WHERE code_insee='33099'").fetchone(),
                         (None, 'non_resolu_dans_extrait_na'))
        self.assertEqual(con.execute('SELECT temperature_2m_max,precipitation_sum FROM fait_meteo_jour').fetchone(), (0.0, 0.0))
        self.assertEqual(con.execute('SELECT modele,latitude,fuseau FROM point_meteo').fetchone(), (None, None, None))
        raw, digest = con.execute("SELECT contenu_gzip,sha256 FROM import_fichier WHERE chemin_relatif='incendies.csv'").fetchone()
        self.assertEqual(gzip.decompress(raw), (self.data / 'incendies.csv').read_bytes())
        self.assertEqual(hashlib.sha256(gzip.decompress(raw)).hexdigest(), digest)

    def test_uncovered_days_stay_unknown_until_explicit_coverage_validation(self):
        self.build()
        con = self.connect()
        query = "SELECT nb_fiches_observees,statut_observation FROM v_jour_departement WHERE code_departement='33' AND date_jour=?"
        self.assertEqual(con.execute(query, ('2026-07-01',)).fetchone(), (None, 'inconnu'))
        self.assertEqual(con.execute(query, ('2025-06-02',)).fetchone(), (None, 'inconnu'))
        with self.assertRaises(sqlite3.IntegrityError):
            con.execute("UPDATE couverture_incendie SET statut='validee_complete' WHERE annee=2025")
        con.execute("UPDATE couverture_incendie SET statut='validee_complete',justification='Confirmation de test',auteur_validation='Test',date_validation='2026-11-21' WHERE annee=2025")
        self.assertEqual(con.execute(query, ('2025-06-02',)).fetchone(), (0, 'couverture_confirmee'))
        self.assertEqual(con.execute(query, ('2026-07-01',)).fetchone(), (None, 'inconnu'))

    def test_hypothesis_dates_are_not_validated_and_require_provenance(self):
        self.build()
        con = self.connect()
        row = con.execute('SELECT date_validite_proposee,date_validite_confirmee,statut_alignement FROM fait_prevision_danger WHERE echeance_j=1').fetchone()
        # UTC le 1er juin à 23:30 est déjà le 2 juin à Paris : J+1 proposé = 3 juin.
        self.assertEqual(row, ('2025-06-03', None, 'non_verifie'))
        self.assertEqual(con.execute('SELECT COUNT(*) FROM v_appariement_j1_valide').fetchone()[0], 0)
        with self.assertRaises(sqlite3.IntegrityError):
            con.execute("UPDATE fait_prevision_danger SET statut_alignement='valide',date_validite_confirmee=date_validite_proposee")
        with self.assertRaises(sqlite3.IntegrityError):
            con.execute('UPDATE fait_prevision_danger SET niveau=5')

    def test_duplicate_input_fails_without_replacing_existing_database(self):
        self.build()
        previous = self.output.read_bytes()
        self.fires.append(self.fires[0].copy())
        self.write_fires()
        with self.assertRaises(sqlite3.IntegrityError):
            self.build(replace=True)
        self.assertEqual(self.output.read_bytes(), previous)
        self.assertFalse(list(self.root.glob('*.tmp')))

    def test_rebuild_is_explicit_and_does_not_accumulate_rows(self):
        self.build()
        with self.assertRaises(FileExistsError):
            self.build()
        report = self.build(replace=True)
        self.assertEqual(report['tables']['fait_incendie'], 1)
        self.assertEqual(report['tables']['fait_prevision_danger'], 2)
        self.assertEqual(report['tables']['fait_meteo_jour'], 1)

    def test_foreign_keys_and_input_ranges_are_enforced(self):
        self.build()
        con = self.connect()
        with self.assertRaises(sqlite3.IntegrityError):
            con.execute("UPDATE fait_incendie SET code_departement='99'")
        with self.assertRaises(sqlite3.IntegrityError):
            con.execute('UPDATE fait_incendie SET surface_parcourue_m2=-1')
        self.assertEqual(con.execute('PRAGMA foreign_key_check').fetchall(), [])
        self.assertEqual(con.execute('PRAGMA integrity_check').fetchone()[0], 'ok')

    def test_invalid_numeric_or_weather_key_fails_without_output(self):
        self.fires[0][6] = 'NaN'
        self.write_fires()
        with self.assertRaises(ValueError):
            self.build()
        self.assertFalse(self.output.exists())
        self.fires[0][6] = '10000'
        self.write_fires()
        self.write('meteo_quotidienne/33.csv', ['date', 'departement', *VARIABLES_METEO],
                   [['2025-06-01', '40', *(['1'] * 8)]], ',')
        with self.assertRaises(ValueError):
            self.build()
        self.assertFalse(self.output.exists())

    def test_department_codes_remain_text(self):
        self.assertEqual(department('1'), '01')
        self.assertEqual(department('2a'), '2A')
        self.assertEqual(department('971'), '971')
        with self.assertRaises(ValueError):
            department('1.0')


if __name__ == '__main__':
    unittest.main()
