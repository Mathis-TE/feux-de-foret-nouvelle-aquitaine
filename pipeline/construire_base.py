"""Construit une base SQLite traçable sans téléchargement ni zéro implicite.

Bibliothèque standard uniquement. Exécution :
    python pipeline/construire_base.py --output data/feux_foret.sqlite
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import os
import sqlite3
import tempfile
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

RACINE = Path(__file__).resolve().parents[1]
DEPARTEMENTS_NA = {'16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87'}
VARIABLES_METEO = (
    'temperature_2m_max', 'temperature_2m_mean', 'precipitation_sum',
    'wind_speed_10m_max', 'wind_gusts_10m_max', 'relative_humidity_2m_min',
    'et0_fao_evapotranspiration', 'soil_moisture_0_to_7cm_mean',
)
SOURCES = (
    ('bdiff', 'BDIFF', 'Ministère chargé de l’Agriculture / IGN',
     'https://bdiff.agriculture.gouv.fr/', 'Licence Ouverte 2.0 affichée au catalogue',
     'Mentions légales jointes plus restrictives : contradiction à clarifier avant redistribution.'),
    ('mdf', 'Archives de la Météo des forêts', 'Météo-France',
     'https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets',
     'Licence Ouverte 2.0', 'Horodatage et dates de validité à confirmer.'),
    ('geo', 'API Découpage administratif', 'DINUM / données INSEE',
     'https://geo.api.gouv.fr/', 'Licence Ouverte annoncée par la fiche du groupe',
     'Millésime exact, unité de superficie et population de l’extrait à confirmer.'),
    ('openmeteo', 'Open-Meteo Historical Weather', 'Open-Meteo / fournisseurs de réanalyses',
     'https://open-meteo.com/en/docs/historical-weather-api', 'CC BY 4.0',
     'Point effectivement renvoyé, modèle, fuseau et unités non attestés dans les CSV transformés.'),
)


def optional(value):
    return value.strip() if value is not None and value.strip() else None


def number(value, integer=False):
    text = optional(value)
    if text is None:
        return None
    try:
        parsed = Decimal(text.replace('\u00a0', '').replace('\u202f', '').replace(',', '.'))
    except InvalidOperation as exc:
        raise ValueError(f'Nombre invalide : {value!r}') from exc
    if not parsed.is_finite():
        raise ValueError(f'Nombre non fini : {value!r}')
    if integer:
        if parsed != parsed.to_integral_value():
            raise ValueError(f'Entier attendu : {value!r}')
        return int(parsed)
    result = float(parsed)
    if not math.isfinite(result):
        raise ValueError(f'Nombre trop grand : {value!r}')
    return result


def department(value):
    text = str(value).strip().upper()
    if text.isdigit() and len(text) <= 2:
        text = text.zfill(2)
    if not (text in {'2A', '2B'} or text.isdigit() and len(text) in {2, 3}):
        raise ValueError(f'Département invalide : {value!r}')
    return text


class Builder:
    def __init__(self, connection, data_dir):
        self.db = connection
        self.data_dir = Path(data_dir)
        self.days = set()
        self.departments = set()
        self.communes = {}
        self.problems = []
        self.imported = []
        try:
            self.paris = ZoneInfo('Europe/Paris')
        except ZoneInfoNotFoundError:
            self.paris = None
            self.warn('FUSEAU_IANA_ABSENT', 'Dates proposées non calculées : Europe/Paris indisponible.')

    def warn(self, code, message, **details):
        self.problems.append({'code': code, 'message': message, **details})
        self.db.execute('''INSERT INTO controle_qualite
            (import_id,entite,cle_entite,code,gravite,message) VALUES (?,?,?,?,?,?)''',
            (details.get('import_id'), 'fichier_source', str(details.get('ligne')) if details.get('ligne') else None,
             code, 'avertissement', message + (' ' + json.dumps(details, ensure_ascii=False) if details else '')))

    def ensure_day(self, value):
        day = date.fromisoformat(value)
        key = day.isoformat()
        if key not in self.days:
            self.db.execute('INSERT INTO dim_date VALUES (?,?,?,?,?)',
                            (key, day.year, day.month, day.day, day.isoweekday()))
            self.days.add(key)
        return key

    def ensure_department(self, code, name=None):
        code = department(code)
        if code not in self.departments:
            self.db.execute('INSERT INTO dim_departement VALUES (?,?,?)',
                            (code, name, int(code in DEPARTEMENTS_NA)))
            self.departments.add(code)
        elif name:
            self.db.execute('UPDATE dim_departement SET nom = COALESCE(nom,?) WHERE code_departement=?', (name, code))
        return code

    def load(self, relative, source, required, preamble=False):
        path = self.data_dir / relative
        raw = path.read_bytes()
        text = raw.decode('utf-8-sig')
        stream = io.StringIO(text, newline='')
        skipped = 0
        if preamble:
            while True:
                pos = stream.tell()
                line = stream.readline()
                if not line:
                    raise ValueError(f'{relative} : en-tête BDIFF introuvable')
                if line.lstrip('\ufeff').startswith('Année;'):
                    stream.seek(pos)
                    break
                skipped += 1
        sample = stream.read(12000)
        stream.seek(0)
        for _ in range(skipped):
            stream.readline()
        dialect = csv.Sniffer().sniff(sample, delimiters=';,\t')
        reader = csv.DictReader(stream, dialect=dialect)
        if not set(required).issubset(reader.fieldnames or []):
            raise ValueError(f'{relative} : colonnes absentes {set(required)-set(reader.fieldnames or [])}')
        rows = []
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'{relative} ligne {reader.line_num + skipped} : nombre de colonnes invalide')
            rows.append((reader.line_num + skipped, row))
        digest = hashlib.sha256(raw).hexdigest()
        cursor = self.db.execute(
            '''INSERT INTO import_fichier
            (source_id,chemin_relatif,sha256,taille_octets,date_import_utc,etat_entree,
             encodage,separateur,lignes_preambule,colonnes_json,nb_lignes,nb_chargees,contenu_gzip)
            VALUES (?,?,?,?,?,?,?,?,?,?,0,0,?)''',
            (source, relative.as_posix(), digest, len(raw), datetime.now(timezone.utc).isoformat(),
             'fichier_du_projet', 'utf-8-sig', dialect.delimiter, skipped,
             json.dumps(reader.fieldnames, ensure_ascii=False), gzip.compress(raw, mtime=0)))
        import_id = cursor.lastrowid
        self.db.execute('UPDATE import_fichier SET nb_lignes=? WHERE import_id=?', (len(rows), import_id))
        self.imported.append((import_id, relative.as_posix(), len(rows)))
        return import_id, rows

    def finish(self, import_id, count):
        self.db.execute('UPDATE import_fichier SET nb_chargees=? WHERE import_id=?', (count, import_id))

    def load_communes(self):
        imp, rows = self.load(Path('communes_na.csv'), 'geo',
                              ['code_insee', 'commune', 'departement', 'lat', 'lon', 'surface_ha', 'population'])
        for line, r in rows:
            dep = self.ensure_department(r['departement'])
            code = r['code_insee'].strip()
            if len(code) != 5:
                raise ValueError(f'Code INSEE invalide à la ligne {line}')
            self.db.execute('''INSERT INTO dim_commune
                (code_insee,code_departement,nom_reference,latitude_centre,longitude_centre,
                 surface_ha_declaree,population_reference,statut_reference,import_id,ligne_csv)
                VALUES (?,?,?,?,?,?,?,?,?,?)''',
                (code, dep, r['commune'], number(r['lat']), number(r['lon']),
                 number(r['surface_ha']), number(r['population'], True),
                 'extrait_communes_fourni', imp, line))
            self.communes[code] = dep
        self.finish(imp, len(rows))
        self.warn('MILLESIME_GEO_INCONNU', 'Millésime et unité officielle de superficie non confirmés ; coordonnées de centres communaux uniquement.')

    def load_fires(self):
        imp, rows = self.load(Path('incendies.csv'), 'bdiff',
                              ['Année', 'Numéro', 'Département', 'Code INSEE', 'Nom de la commune',
                               'Date de première alerte', 'Surface parcourue (m2)', 'Surface forêt (m2)'], True)
        partial, causes_missing, stubs = 0, 0, set()
        for line, r in rows:
            dep = self.ensure_department(r['Département'])
            code = r['Code INSEE'].strip()
            if len(code) != 5:
                raise ValueError(f'BDIFF ligne {line} : code INSEE invalide')
            if code not in self.communes:
                status = 'non_resolu_dans_extrait_na' if dep in DEPARTEMENTS_NA else 'hors_extrait_na'
                self.db.execute('''INSERT INTO dim_commune
                    (code_insee,code_departement,nom_reference,statut_reference,import_id,ligne_csv)
                    VALUES (?,?,?,?,?,?)''', (code, dep, r['Nom de la commune'], status, imp, line))
                self.communes[code] = dep
                stubs.add(code)
            if self.communes[code] != dep or not code.startswith(dep):
                raise ValueError(f'BDIFF ligne {line} : commune et département incohérents')
            year = number(r['Année'], True)
            alert = datetime.fromisoformat(r['Date de première alerte'].strip())
            if alert.year != year or alert.tzinfo is not None:
                raise ValueError(f'BDIFF ligne {line} : année/fuseau inattendu')
            day = self.ensure_day(alert.date().isoformat())
            cause = optional(r.get('Nature'))
            if cause:
                self.db.execute('INSERT OR IGNORE INTO dim_cause VALUES (?)', (cause,))
            else:
                causes_missing += 1
            consequence = optional(r.get('Décès ou bâtiments touchés'))
            if consequence not in {None, 'Oui', 'Non'}:
                raise ValueError(f'BDIFF ligne {line} : conséquence non reconnue')
            precision = optional(r.get('Précision de la donnée'))
            partial += int(precision is not None)
            area = number(r['Surface parcourue (m2)'])
            forest = number(r['Surface forêt (m2)'])
            if area is not None and forest is not None and forest > area:
                self.warn('SURFACE_INCOHERENTE', 'Surface forêt supérieure au total.', import_id=imp, ligne=line)
            self.db.execute('''INSERT INTO fait_incendie
                (incendie_id,annee,numero_source,code_departement,code_insee,nom_commune_source,
                 alerte_source,jour_alerte,surface_parcourue_m2,surface_foret_m2,cause,
                 precision_surfaces,precision_donnee,type_peuplement,consequence_signalee,
                 nombre_deces,batiments_detruits,batiments_partiellement_detruits,import_id,ligne_csv)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (f"{year}-{r['Numéro']}", year, r['Numéro'], dep, code, r['Nom de la commune'],
                 r['Date de première alerte'], day, area, forest, cause,
                 optional(r.get('Précision des surfaces')), precision, optional(r.get('Type de peuplement')),
                 None if consequence is None else int(consequence == 'Oui'),
                 number(r.get('Nombre de décès'), True), number(r.get('Nombre de bâtiments totalement détruits'), True),
                 number(r.get('Nombre de bâtiments partiellement détruits'), True), imp, line))
        self.finish(imp, len(rows))
        self.warn('COUVERTURE_BDIFF_NON_VALIDEE', 'Aucune campagne n’est déclarée complète automatiquement ; fuseau des alertes non confirmé.')
        self.warn('PRECISION_DONNEE_SOURCE', 'Signalements source conservés sans exclusion automatique.', nombre=partial)
        self.warn('CAUSE_NON_RENSEIGNEE', 'Causes vides conservées à NULL.', nombre=causes_missing)
        self.warn('COMMUNES_NON_REFERENCEES', 'Communes des feux conservées sans géolocalisation inventée.', nombre=len(stubs),
                  non_resolues_na=sum(self.communes[c] in DEPARTEMENTS_NA for c in stubs))
        return imp, min(int(r['Année']) for _, r in rows), max(int(r['Année']) for _, r in rows)

    def load_danger(self):
        imp, rows = self.load(Path('meteo_foret_na.csv'), 'mdf', ['date', 'num_dep', 'niveau_j1', 'niveau_j2'])
        for line, r in rows:
            name = optional(r.get('nom_dep')) or optional(r.get('dep_nom'))
            dep = self.ensure_department(r['num_dep'], name)
            stamp = datetime.fromisoformat(r['date'].replace('Z', '+00:00'))
            if stamp.tzinfo is None:
                raise ValueError(f'Météo des forêts ligne {line} : fuseau absent')
            stamp_utc = stamp.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
            cur = self.db.execute('''INSERT INTO bulletin_danger
                (code_departement,horodatage_source_utc,nom_departement_source,import_id,ligne_csv)
                VALUES (?,?,?,?,?)''', (dep, stamp_utc, name, imp, line))
            for horizon in (1, 2):
                proposed = None
                if self.paris:
                    proposed = self.ensure_day((stamp.astimezone(self.paris).date() + timedelta(days=horizon)).isoformat())
                level = number(r[f'niveau_j{horizon}'], True)
                self.db.execute('''INSERT INTO fait_prevision_danger
                    (bulletin_id,echeance_j,niveau,date_validite_proposee) VALUES (?,?,?,?)''',
                    (cur.lastrowid, horizon, level, proposed))
        self.finish(imp, len(rows))
        self.warn('ALIGNEMENT_MDF_NON_VALIDE', 'Deux échéances conservées. Dates proposées sous hypothèse émission, dates confirmées à NULL.', bulletins=len(rows))

    def load_weather(self):
        paths = sorted((self.data_dir / 'meteo_quotidienne').glob('*.csv'))
        if not paths:
            raise ValueError('Aucun fichier meteo_quotidienne/*.csv')
        for path in paths:
            imp, rows = self.load(path.relative_to(self.data_dir), 'openmeteo', ['date', 'departement', *VARIABLES_METEO])
            declared = department(path.stem)
            dep = self.ensure_department(declared)
            point = f'openmeteo:{dep}:import:{imp}'
            self.db.execute('INSERT INTO point_meteo(point_id,code_departement,import_id) VALUES (?,?,?)', (point, dep, imp))
            for line, r in rows:
                if department(r['departement']) != dep:
                    raise ValueError(f'{path.name} ligne {line} : département différent du fichier')
                day = self.ensure_day(r['date'])
                values = [number(r[k]) for k in VARIABLES_METEO]
                self.db.execute('INSERT INTO fait_meteo_jour VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                                (point, day, *values, imp, line))
            self.finish(imp, len(rows))
        self.warn('PROVENANCE_METEO_INCOMPLETE', 'Point renvoyé, modèle, fuseau et unités non attestés : métadonnées laissées à NULL.', fichiers=len(paths))

    def calendar_and_coverage(self, bdiff_import, first_year, last_year, calendar_end):
        first = date.fromisoformat(min(self.days))
        end = max(date.fromisoformat(max(self.days)), date.fromisoformat(calendar_end))
        day = first
        while day <= end:
            self.ensure_day(day.isoformat())
            day += timedelta(days=1)
        for dep in sorted(self.departments):
            for year in range(first.year, end.year + 1):
                present = first_year <= year <= last_year
                status = 'non_verifiee' if present else 'hors_periode_importee'
                reason = ('La présence de fiches ne certifie pas l’exhaustivité départementale.' if present
                          else 'Année hors des bornes de l’historique BDIFF importé ; aucune absence de feu déduite.')
                self.db.execute('''INSERT INTO couverture_incendie
                    (code_departement,annee,statut,justification,import_id) VALUES (?,?,?,?,?)''',
                    (dep, year, status, reason, bdiff_import))

    def report(self):
        names = ['source_donnee', 'import_fichier', 'dim_departement', 'dim_commune', 'dim_date',
                 'fait_incendie', 'bulletin_danger', 'fait_prevision_danger', 'point_meteo', 'fait_meteo_jour',
                 'couverture_incendie', 'dispositif_renforcement', 'activation_dispositif', 'disponibilite_moyens', 'budget_saison']
        integrity = self.db.execute('PRAGMA integrity_check').fetchall()
        foreign_keys = self.db.execute('PRAGMA foreign_key_check').fetchall()
        if integrity != [('ok',)] or foreign_keys:
            raise ValueError(f'Intégrité invalide : {integrity}, {foreign_keys}')
        for imp, path, expected in self.imported:
            loaded = self.db.execute('SELECT nb_chargees FROM import_fichier WHERE import_id=?', (imp,)).fetchone()[0]
            if loaded != expected:
                raise ValueError(f'{path} : {loaded}/{expected} lignes chargées')
        for digest, raw in self.db.execute('SELECT sha256,contenu_gzip FROM import_fichier'):
            if hashlib.sha256(gzip.decompress(raw)).hexdigest() != digest:
                raise ValueError('Archive source corrompue')
        return {
            'schema_version': 1, 'sqlite_version': sqlite3.sqlite_version,
            'date_construction_utc': datetime.now(timezone.utc).isoformat(),
            'tables': {name: self.db.execute(f'SELECT COUNT(*) FROM {name}').fetchone()[0] for name in names},
            'integrity_check': 'ok', 'foreign_key_errors': 0, 'archives_sources_sha256': 'valides',
            'periodes': {
                'incendies': list(self.db.execute('SELECT MIN(alerte_source),MAX(alerte_source) FROM fait_incendie').fetchone()),
                'danger_horodatage_source': list(self.db.execute('SELECT MIN(horodatage_source_utc),MAX(horodatage_source_utc) FROM bulletin_danger').fetchone()),
                'meteo': list(self.db.execute('SELECT MIN(date_jour),MAX(date_jour) FROM fait_meteo_jour').fetchone()),
            },
            'gironde': {
                'incendies': self.db.execute("SELECT COUNT(*) FROM fait_incendie WHERE code_departement='33'").fetchone()[0],
                'bulletins': self.db.execute("SELECT COUNT(*) FROM bulletin_danger WHERE code_departement='33'").fetchone()[0],
                'jours_meteo': self.db.execute("SELECT COUNT(*) FROM fait_meteo_jour f JOIN point_meteo p USING(point_id) WHERE p.code_departement='33'").fetchone()[0],
            },
            'avertissements': self.problems,
            'portee': 'BDIFF national ; référentiel et danger régionaux ; météo des points déclarés par département. Données opérationnelles non fournies.',
        }


def build_database(data_dir, output, *, replace=False, calendar_end='2027-12-31', schema_path=None):
    data_dir, output = Path(data_dir).resolve(), Path(output).resolve()
    if output.suffix.lower() not in {'.sqlite', '.sqlite3', '.db'}:
        raise ValueError('Le fichier de sortie doit porter une extension SQLite, pas celle d’un fichier source.')
    if output.exists() and not replace:
        raise FileExistsError(f'{output} existe déjà ; utiliser --replace pour reconstruire explicitement.')
    output.parent.mkdir(parents=True, exist_ok=True)
    schema_path = Path(schema_path) if schema_path else RACINE / 'sql/schema_sqlite.sql'
    handle, temporary_name = tempfile.mkstemp(prefix=output.name + '.', suffix='.tmp', dir=output.parent)
    os.close(handle)
    temporary = Path(temporary_name)
    connection = None
    try:
        connection = sqlite3.connect(temporary)
        connection.execute('PRAGMA foreign_keys=ON')
        connection.executescript(schema_path.read_text(encoding='utf-8'))
        with connection:
            connection.executemany('INSERT INTO source_donnee VALUES (?,?,?,?,?,?)', SOURCES)
            connection.executemany('INSERT INTO dim_niveau_danger VALUES (?,?)', [(1, 'faible'), (2, 'modere'), (3, 'eleve'), (4, 'tres_eleve')])
            builder = Builder(connection, data_dir)
            builder.load_communes()
            imp, first, last = builder.load_fires()
            builder.load_danger()
            builder.load_weather()
            builder.calendar_and_coverage(imp, first, last, calendar_end)
            report = builder.report()
        connection.execute('ANALYZE')
        connection.commit()
        connection.close()
        connection = None
        if replace:
            os.replace(temporary, output)
        elif os.name == 'nt':
            # Sous Windows rename échoue si la destination existe ; pas de lien
            # physique, qui n'est pas autorisé par certains bacs à sable.
            os.rename(temporary, output)
        else:
            os.link(temporary, output)
            temporary.unlink()
        report['fichier_base'] = output.name
        report['taille_octets'] = output.stat().st_size
        report['sha256_base'] = hashlib.sha256(output.read_bytes()).hexdigest()
        return report
    except Exception:
        if connection is not None:
            connection.close()
        temporary.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=RACINE / 'data')
    parser.add_argument('--output', type=Path, default=RACINE / 'data/feux_foret.sqlite')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--fin-calendrier', default='2027-12-31')
    parser.add_argument('--replace', action='store_true')
    args = parser.parse_args()
    destination = args.report or args.output.with_suffix('.rapport.json')
    if destination.suffix.lower() != '.json' or destination.resolve() == args.output.resolve():
        parser.error('Le rapport doit être un fichier JSON distinct de la base et des CSV sources.')
    report = build_database(args.data_dir, args.output, replace=args.replace, calendar_end=args.fin_calendrier)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'base': str(args.output), 'rapport': str(destination), 'tables': report['tables']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
