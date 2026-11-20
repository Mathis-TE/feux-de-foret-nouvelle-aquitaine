-- Base SQLite v1. Les dates proposées ne constituent pas des dates validées.
PRAGMA foreign_keys = ON;
PRAGMA user_version = 1;

CREATE TABLE source_donnee (
    source_id TEXT PRIMARY KEY,
    libelle TEXT NOT NULL,
    producteur TEXT NOT NULL,
    url TEXT NOT NULL,
    licence_declaree TEXT,
    reserve_reutilisation TEXT
);

CREATE TABLE import_fichier (
    import_id INTEGER PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES source_donnee,
    chemin_relatif TEXT NOT NULL UNIQUE,
    sha256 TEXT NOT NULL CHECK(length(sha256) = 64),
    taille_octets INTEGER NOT NULL CHECK(taille_octets >= 0),
    date_import_utc TEXT NOT NULL,
    date_collecte_source TEXT,
    etat_entree TEXT NOT NULL CHECK(etat_entree IN ('fichier_du_projet', 'documentation')),
    encodage TEXT,
    separateur TEXT,
    lignes_preambule INTEGER NOT NULL DEFAULT 0,
    colonnes_json TEXT,
    nb_lignes INTEGER NOT NULL DEFAULT 0 CHECK(nb_lignes >= 0),
    nb_chargees INTEGER NOT NULL DEFAULT 0 CHECK(nb_chargees >= 0),
    contenu_gzip BLOB NOT NULL
);

CREATE TABLE controle_qualite (
    controle_id INTEGER PRIMARY KEY,
    import_id INTEGER REFERENCES import_fichier,
    entite TEXT NOT NULL,
    cle_entite TEXT,
    code TEXT NOT NULL,
    gravite TEXT NOT NULL CHECK(gravite IN ('information', 'avertissement')),
    message TEXT NOT NULL
);

CREATE TABLE dim_departement (
    code_departement TEXT PRIMARY KEY CHECK(length(code_departement) IN (2, 3)),
    nom TEXT,
    est_nouvelle_aquitaine INTEGER NOT NULL CHECK(est_nouvelle_aquitaine IN (0, 1))
);

CREATE TABLE dim_date (
    date_jour TEXT PRIMARY KEY,
    annee INTEGER NOT NULL,
    mois INTEGER NOT NULL CHECK(mois BETWEEN 1 AND 12),
    jour INTEGER NOT NULL CHECK(jour BETWEEN 1 AND 31),
    jour_semaine_iso INTEGER NOT NULL CHECK(jour_semaine_iso BETWEEN 1 AND 7)
);

CREATE TABLE dim_commune (
    code_insee TEXT PRIMARY KEY CHECK(length(code_insee) = 5),
    code_departement TEXT NOT NULL REFERENCES dim_departement,
    nom_reference TEXT NOT NULL,
    latitude_centre REAL CHECK(latitude_centre BETWEEN -90 AND 90),
    longitude_centre REAL CHECK(longitude_centre BETWEEN -180 AND 180),
    surface_ha_declaree REAL CHECK(surface_ha_declaree >= 0),
    unite_surface_confirmee INTEGER NOT NULL DEFAULT 0 CHECK(unite_surface_confirmee IN (0, 1)),
    population_reference INTEGER CHECK(population_reference >= 0),
    millesime_reference INTEGER,
    statut_reference TEXT NOT NULL CHECK(statut_reference IN (
        'extrait_communes_fourni', 'non_resolu_dans_extrait_na', 'hors_extrait_na')),
    import_id INTEGER NOT NULL REFERENCES import_fichier,
    ligne_csv INTEGER NOT NULL CHECK(ligne_csv > 0)
);

-- Aucune correspondance historique n'est inventée à partir d'un nom voisin.
CREATE TABLE correspondance_commune (
    code_ancien TEXT NOT NULL,
    code_actuel TEXT NOT NULL REFERENCES dim_commune,
    valide_depuis TEXT,
    valide_jusqua TEXT,
    reference_officielle TEXT NOT NULL,
    PRIMARY KEY(code_ancien, code_actuel, reference_officielle)
);

CREATE TABLE dim_cause (libelle TEXT PRIMARY KEY);
CREATE TABLE dim_niveau_danger (
    niveau INTEGER PRIMARY KEY CHECK(niveau BETWEEN 1 AND 4),
    libelle TEXT NOT NULL UNIQUE
);

CREATE TABLE fait_incendie (
    incendie_id TEXT PRIMARY KEY,
    annee INTEGER NOT NULL,
    numero_source TEXT NOT NULL,
    code_departement TEXT NOT NULL REFERENCES dim_departement,
    code_insee TEXT NOT NULL REFERENCES dim_commune,
    nom_commune_source TEXT NOT NULL,
    alerte_source TEXT NOT NULL,
    jour_alerte TEXT NOT NULL REFERENCES dim_date(date_jour),
    fuseau_alerte TEXT,
    surface_parcourue_m2 REAL CHECK(surface_parcourue_m2 >= 0),
    surface_foret_m2 REAL CHECK(surface_foret_m2 >= 0),
    cause TEXT REFERENCES dim_cause(libelle),
    precision_surfaces TEXT,
    precision_donnee TEXT,
    type_peuplement TEXT,
    consequence_signalee INTEGER CHECK(consequence_signalee IN (0, 1)),
    nombre_deces INTEGER CHECK(nombre_deces >= 0),
    batiments_detruits INTEGER CHECK(batiments_detruits >= 0),
    batiments_partiellement_detruits INTEGER CHECK(batiments_partiellement_detruits >= 0),
    import_id INTEGER NOT NULL REFERENCES import_fichier,
    ligne_csv INTEGER NOT NULL CHECK(ligne_csv > 0),
    UNIQUE(annee, numero_source),
    UNIQUE(import_id, ligne_csv)
);

CREATE TABLE bulletin_danger (
    bulletin_id INTEGER PRIMARY KEY,
    code_departement TEXT NOT NULL REFERENCES dim_departement,
    horodatage_source_utc TEXT NOT NULL,
    nom_departement_source TEXT,
    import_id INTEGER NOT NULL REFERENCES import_fichier,
    ligne_csv INTEGER NOT NULL CHECK(ligne_csv > 0),
    UNIQUE(code_departement, horodatage_source_utc),
    UNIQUE(import_id, ligne_csv)
);

CREATE TABLE fait_prevision_danger (
    bulletin_id INTEGER NOT NULL REFERENCES bulletin_danger,
    echeance_j INTEGER NOT NULL CHECK(echeance_j IN (1, 2)),
    niveau INTEGER NOT NULL REFERENCES dim_niveau_danger,
    date_validite_proposee TEXT REFERENCES dim_date(date_jour),
    date_validite_confirmee TEXT REFERENCES dim_date(date_jour),
    statut_alignement TEXT NOT NULL DEFAULT 'non_verifie'
        CHECK(statut_alignement IN ('non_verifie', 'valide', 'rejete')),
    auteur_validation TEXT,
    reference_validation TEXT,
    date_validation TEXT,
    PRIMARY KEY(bulletin_id, echeance_j),
    CHECK((statut_alignement = 'valide' AND date_validite_confirmee IS NOT NULL
           AND auteur_validation IS NOT NULL AND length(trim(auteur_validation)) > 0
           AND reference_validation IS NOT NULL AND length(trim(reference_validation)) > 0
           AND date_validation IS NOT NULL)
       OR (statut_alignement <> 'valide' AND date_validite_confirmee IS NULL))
);

-- Le point effectivement renvoyé par Open-Meteo n'est pas conservé dans les CSV.
CREATE TABLE point_meteo (
    point_id TEXT PRIMARY KEY,
    code_departement TEXT NOT NULL REFERENCES dim_departement,
    import_id INTEGER NOT NULL UNIQUE REFERENCES import_fichier,
    latitude REAL CHECK(latitude BETWEEN -90 AND 90),
    longitude REAL CHECK(longitude BETWEEN -180 AND 180),
    modele TEXT,
    fuseau TEXT,
    unites_attestees INTEGER NOT NULL DEFAULT 0 CHECK(unites_attestees IN (0, 1)),
    statut_provenance TEXT NOT NULL DEFAULT 'incomplet'
        CHECK(statut_provenance IN ('incomplet', 'documente')),
    CHECK((latitude IS NULL AND longitude IS NULL) OR (latitude IS NOT NULL AND longitude IS NOT NULL))
);

CREATE TABLE fait_meteo_jour (
    point_id TEXT NOT NULL REFERENCES point_meteo,
    date_jour TEXT NOT NULL REFERENCES dim_date,
    temperature_2m_max REAL,
    temperature_2m_mean REAL,
    precipitation_sum REAL,
    wind_speed_10m_max REAL,
    wind_gusts_10m_max REAL,
    relative_humidity_2m_min REAL,
    et0_fao_evapotranspiration REAL,
    soil_moisture_0_to_7cm_mean REAL,
    import_id INTEGER NOT NULL REFERENCES import_fichier,
    ligne_csv INTEGER NOT NULL CHECK(ligne_csv > 0),
    PRIMARY KEY(point_id, date_jour),
    UNIQUE(import_id, ligne_csv)
);

CREATE TABLE couverture_incendie (
    code_departement TEXT NOT NULL REFERENCES dim_departement,
    annee INTEGER NOT NULL,
    statut TEXT NOT NULL CHECK(statut IN ('non_verifiee', 'validee_complete', 'incomplete', 'hors_periode_importee')),
    justification TEXT NOT NULL,
    auteur_validation TEXT,
    date_validation TEXT,
    import_id INTEGER NOT NULL REFERENCES import_fichier,
    PRIMARY KEY(code_departement, annee),
    CHECK(statut <> 'validee_complete' OR
          (auteur_validation IS NOT NULL AND length(trim(auteur_validation)) > 0 AND date_validation IS NOT NULL))
);

-- Structures opérationnelles prévues, sans observations inventées.
CREATE TABLE dispositif_renforcement (
    dispositif_id INTEGER PRIMARY KEY,
    libelle TEXT NOT NULL,
    description TEXT NOT NULL,
    reference_source TEXT NOT NULL
);
CREATE TABLE activation_dispositif (
    activation_id INTEGER PRIMARY KEY,
    dispositif_id INTEGER NOT NULL REFERENCES dispositif_renforcement,
    code_departement TEXT NOT NULL REFERENCES dim_departement,
    secteur TEXT NOT NULL,
    debut TEXT NOT NULL,
    fin TEXT NOT NULL CHECK(fin > debut),
    effectif INTEGER CHECK(effectif >= 0),
    nombre_engins INTEGER CHECK(nombre_engins >= 0),
    cout_additionnel_centimes INTEGER CHECK(cout_additionnel_centimes >= 0),
    reference_source TEXT NOT NULL
);
CREATE TABLE disponibilite_moyens (
    disponibilite_id INTEGER PRIMARY KEY,
    code_departement TEXT NOT NULL REFERENCES dim_departement,
    secteur TEXT NOT NULL,
    debut TEXT NOT NULL,
    fin TEXT NOT NULL CHECK(fin > debut),
    effectif_disponible INTEGER CHECK(effectif_disponible >= 0),
    engins_disponibles INTEGER CHECK(engins_disponibles >= 0),
    reference_source TEXT NOT NULL
);
CREATE TABLE budget_saison (
    code_departement TEXT NOT NULL REFERENCES dim_departement,
    annee INTEGER NOT NULL,
    montant_affectable_centimes INTEGER NOT NULL CHECK(montant_affectable_centimes >= 0),
    reference_source TEXT NOT NULL,
    PRIMARY KEY(code_departement, annee)
);

CREATE INDEX incendie_departement_jour ON fait_incendie(code_departement, jour_alerte);
CREATE INDEX incendie_commune_annee ON fait_incendie(code_insee, annee);
CREATE INDEX bulletin_departement ON bulletin_danger(code_departement, horodatage_source_utc);
CREATE INDEX prevision_date_proposee ON fait_prevision_danger(date_validite_proposee, echeance_j);
CREATE INDEX prevision_date_confirmee ON fait_prevision_danger(date_validite_confirmee, echeance_j);
CREATE INDEX point_departement ON point_meteo(code_departement);

CREATE VIEW v_imports AS
SELECT import_id, source_id, chemin_relatif, sha256, taille_octets, date_import_utc,
       date_collecte_source, etat_entree, encodage, separateur,
       lignes_preambule, colonnes_json, nb_lignes, nb_chargees
FROM import_fichier;

CREATE VIEW v_incendies_detail AS
SELECT f.*, f.surface_parcourue_m2 / 10000.0 AS surface_parcourue_ha,
       f.surface_foret_m2 / 10000.0 AS surface_foret_ha,
       c.statut_reference AS statut_reference_commune,
       c.latitude_centre AS latitude_centre_communal,
       c.longitude_centre AS longitude_centre_communal
FROM fait_incendie f JOIN dim_commune c USING(code_insee);

CREATE VIEW v_incendies_commune_annee AS
SELECT code_departement, code_insee, annee, COUNT(*) AS nb_fiches_enregistrees,
       SUM(surface_parcourue_m2) / 10000.0 AS surface_parcourue_ha,
       SUM(surface_parcourue_m2 IS NULL) AS nb_surfaces_manquantes
FROM fait_incendie GROUP BY code_departement, code_insee, annee;

CREATE VIEW v_incendies_mois AS
SELECT f.code_departement, d.annee, d.mois, COUNT(*) AS nb_fiches_enregistrees,
       SUM(f.surface_parcourue_m2) / 10000.0 AS surface_parcourue_ha
FROM fait_incendie f JOIN dim_date d ON f.jour_alerte = d.date_jour
GROUP BY f.code_departement, d.annee, d.mois;

-- NULL reste NULL hors couverture confirmée. Un événement présent est un compte
-- de fiches observées, qui peut être incomplet, et non un total garanti de feux.
CREATE VIEW v_jour_departement AS
WITH feux AS (
    SELECT code_departement, jour_alerte, COUNT(*) AS n,
           SUM(surface_parcourue_m2) AS surface_m2
    FROM fait_incendie GROUP BY code_departement, jour_alerte
)
SELECT dep.code_departement, d.date_jour, d.annee,
       CASE WHEN f.n IS NOT NULL THEN f.n
            WHEN c.statut = 'validee_complete' THEN 0 ELSE NULL END AS nb_fiches_observees,
       CASE WHEN f.n IS NOT NULL THEN f.surface_m2 / 10000.0
            WHEN c.statut = 'validee_complete' THEN 0.0 ELSE NULL END AS surface_observee_ha,
       c.statut AS statut_couverture,
       CASE WHEN c.statut = 'validee_complete' THEN 'couverture_confirmee'
            WHEN f.n IS NOT NULL THEN 'fiches_presentes_total_non_garanti'
            ELSE 'inconnu' END AS statut_observation
FROM dim_departement dep CROSS JOIN dim_date d
LEFT JOIN feux f ON f.code_departement = dep.code_departement AND f.jour_alerte = d.date_jour
LEFT JOIN couverture_incendie c ON c.code_departement = dep.code_departement AND c.annee = d.annee;

-- Vue d'exploration explicitement fondée sur une hypothèse, jamais présentée
-- comme une jointure validée pour l'évaluation opérationnelle.
CREATE VIEW v_appariement_j1_a_confirmer AS
SELECT b.code_departement, b.horodatage_source_utc, p.date_validite_proposee,
       p.niveau, p.statut_alignement, j.nb_fiches_observees,
       j.surface_observee_ha, j.statut_couverture, j.statut_observation
FROM fait_prevision_danger p JOIN bulletin_danger b USING(bulletin_id)
LEFT JOIN v_jour_departement j ON j.code_departement = b.code_departement
                              AND j.date_jour = p.date_validite_proposee
WHERE p.echeance_j = 1;

CREATE VIEW v_appariement_j1_valide AS
SELECT b.code_departement, p.date_validite_confirmee AS date_jour, p.niveau,
       j.nb_fiches_observees, j.surface_observee_ha
FROM fait_prevision_danger p JOIN bulletin_danger b USING(bulletin_id)
JOIN v_jour_departement j ON j.code_departement = b.code_departement
                         AND j.date_jour = p.date_validite_confirmee
WHERE p.echeance_j = 1 AND p.statut_alignement = 'valide'
  AND j.statut_couverture = 'validee_complete';
