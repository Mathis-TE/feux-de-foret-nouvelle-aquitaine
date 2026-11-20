-- Exécuter sur feux_foret.sqlite. Comptages de fiches, exhaustivité non garantie.
PRAGMA foreign_keys = ON;

-- Où les incendies enregistrés se concentrent-ils en Gironde ?
SELECT code_insee, COUNT(*) AS nb_fiches,
       SUM(surface_parcourue_m2)/10000.0 AS surface_parcourue_ha
FROM fait_incendie WHERE code_departement='33'
GROUP BY code_insee ORDER BY nb_fiches DESC;

-- Saisonnalité des fiches enregistrées.
SELECT * FROM v_incendies_mois WHERE code_departement='33'
ORDER BY annee, mois;

-- Vérifier la couverture avant toute évaluation de l'indice.
SELECT * FROM couverture_incendie WHERE code_departement='33' ORDER BY annee;
SELECT statut_observation, COUNT(*) AS nb_jours
FROM v_jour_departement WHERE code_departement='33' AND annee=2026
GROUP BY statut_observation;

-- Cette vue reste vide tant que dates de validité et couverture ne sont pas validées.
SELECT * FROM v_appariement_j1_valide WHERE code_departement='33';

-- Provenance et limites à examiner.
SELECT * FROM v_imports;
SELECT * FROM controle_qualite;
