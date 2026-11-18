# Sources de données

Le projet *Feux de forêt Nouvelle-Aquitaine* repose sur **5 sources essentielles**. Chacune tient un rôle que les autres ne couvrent pas :

| Rôle | Source |
|---|---|
| Cible : les feux | 1. BDIFF |
| Indice à évaluer : le seuil de déclenchement | 2. Météo des forêts |
| Référentiel : la clé commune → département | 3. geo.api.gouv.fr |
| Variables explicatives de la prédiction | 4. Open-Meteo |
| Détection par satellite | 5. NASA FIRMS |

Les fiches de qualité et la matrice questions × sources sont dans [`docs/entrepot/03-sources-de-donnees.md`](entrepot/03-sources-de-donnees.md).

## Vue d'ensemble

| # | Source | Producteur | Rôle | Fichier `data/` | Table gold | Licence |
|---|---|---|---|---|---|---|
| 1 | BDIFF, Base de données des incendies de forêt en France | Ministère de l'Agriculture / IGN | Cible | `incendies.csv` | `fait_incendie` | Usage non commercial, avec citation (voir fiche) |
| 2 | Archives de la Météo des forêts | Météo-France | Indice à évaluer | `meteo_foret_na.csv`, `meteo_foret_france.csv` | `fait_prevision_danger` | Licence Ouverte 2.0 |
| 3 | API Découpage administratif (communes) | Etalab / INSEE | Référentiel | `communes_na.csv` | `dim_commune` | Licence Ouverte 2.0 |
| 4 | Open-Meteo Historical Weather (réanalyse ERA5) | Open-Meteo / ECMWF | Variables explicatives | `meteo_quotidienne/<dep>.csv` | `fait_meteo_jour` | CC BY 4.0, API gratuite non commerciale |
| 5 | NASA FIRMS (MODIS / VIIRS) | NASA | Détection | `firms/<capteur>_<année>.csv` | `fait_detection_satellite` | Libre, mention de source demandée |

## Téléchargement local

Les sources 2 à 5 se téléchargent **une seule fois** :

```bash
python pipeline/telecharger_sources.py                       # communes, mdf, openmeteo, firms
python pipeline/telecharger_sources.py --sources mdf,firms   # certaines sources
python pipeline/telecharger_sources.py --forcer mdf          # retélécharger une source
```

- Une fois les fichiers dans `data/`, le notebook et le pipeline ne refont plus d'appel aux API.
- Le script reprend là où il s'est arrêté, relance en cas d'erreur et attend en cas de limite atteinte (code 429).
- Chaque fichier écrit est consigné dans `data/_journal_telechargements.csv` (date, nombre de lignes, empreinte SHA-256).
- FIRMS demande la clé `FIRMS_MAP_KEY` dans le fichier `.env` (non versionné).
- La BDIFF n'a pas d'API : elle s'exporte à la main depuis le site.

---

## 1. BDIFF, Base de données des incendies de forêt en France
- **Lien :** https://bdiff.agriculture.gouv.fr/incendies
- **Producteur :** Ministère de l'Agriculture et de la Souveraineté alimentaire. Site conçu et hébergé par l'IGN.
- **Accès :** export CSV depuis le site (recherche multicritère). Séparateur `;`.
- **Fichiers :**
  - `data/incendies2006-2016/Incendies.csv` et `data/incendies2017-2025/Incendies.csv` : exports bruts, avec `Définitions.pdf` et `Mention légales.pdf` ;
  - `data/incendies.csv` : la concaténation des deux, utilisée par le notebook et le pipeline.
- **Couverture :** France entière, 2006-2025. 52 811 feux, dont 8 947 en Nouvelle-Aquitaine et 3 555 en Gironde.
- **Grain :** un feu (une fiche). La clé est (`Année`, `Numéro`).
- **Contenu :** date et heure de première alerte, commune (code INSEE), surfaces par type de végétation, précision des surfaces, type de peuplement, cause (`Nature`), décès et bâtiments touchés.
- **Pourquoi elle est essentielle :** c'est la seule source officielle et exhaustive des feux de forêt en France. Sans elle, il n'y a ni cible à prédire ni réponse aux questions de la commande.
- **Limites :** cause inconnue dans 49 % des cas en France et 61 % en Gironde ; nomenclature des surfaces changée en 2023 ; aucune donnée pour le 64 en 2010-2011 ; 2024 sans doute incomplète en Gironde ; la commune est la maille la plus fine.
- **Conditions d'utilisation** (`Mention légales.pdf`, §7) :
  - usage autorisé à des fins personnelles, associatives ou professionnelles ;
  - pas de vente ni de redevance, tout usage commercial est exclu ;
  - données intactes ;
  - citer http://bdiff.agriculture.gouv.fr comme source et mentionner que les droits de reproduction sont réservés.
- **Citation proposée :** « Source : BDIFF, bdiff.agriculture.gouv.fr, extraction du [date]. Droits de reproduction réservés et strictement limités. »

## 2. Archives de la Météo des forêts
- **Lien :** https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets
- **Producteur :** Météo-France, en lien avec l'ONF.
- **Accès :** le jeu de données contient un fichier compressé par saison. Le script les télécharge tous (`--sources mdf`).
- **Fichiers :**
  - `data/brut/meteo_des_forets/<id>.csv.gz` : archives brutes, une par ressource du jeu de données ;
  - `data/meteo_foret_france.csv` : toutes les saisons, France entière, pour la question 4 ;
  - `data/meteo_foret_na.csv` : extrait Nouvelle-Aquitaine. Colonnes : `date` (date d'émission), `num_dep`, `niveau_j1`, `niveau_j2`, `nom_dep`.
- **Couverture :** depuis le 3 juin 2024, de juin à septembre. **Seule 2024 est en local pour l'instant.**
- **Grain :** un département × un jour d'émission, avec les niveaux 1 à 4 pour J+1 et J+2.
- **Pourquoi elle est essentielle :** c'est l'indice dont la commande demande d'évaluer le seuil (questions 2 et 3). Aucune autre source ne la remplace.
- **Piège :** la date est celle de l'**émission**. `niveau_j1` vaut pour le lendemain. Le décalage est appliqué dans le notebook comme dans l'entrepôt.
- **Licence :** Licence Ouverte 2.0.

## 3. API Découpage administratif (communes)
- **Lien :** https://geo.api.gouv.fr/decoupage-administratif/communes
- **Requête :** `/departements/{dep}/communes?fields=nom,code,centre,surface,population`.
- **Fichier :** `data/communes_na.csv`, 4 293 communes des 12 départements.
- **Pourquoi elle est essentielle :** c'est la table de jointure du modèle. Elle donne le département et les coordonnées de chaque feu à partir de son code INSEE. Elle sert aussi à placer le point météo de chaque département (centre moyen des communes) et à rattacher chaque détection satellite à une commune.
- **Limite :** référentiel courant ; 137 feux de Nouvelle-Aquitaine portent le code d'une commune fusionnée depuis.
- **Licence :** Licence Ouverte 2.0.

## 4. Open-Meteo Historical Weather (réanalyse ERA5 / ERA5-Land)
- **Lien :** https://open-meteo.com/en/docs/historical-weather-api. Point d'accès `https://archive-api.open-meteo.com/v1/archive`.
- **Fichiers :** `data/meteo_quotidienne/<dep>.csv`, un point par département (centre moyen des communes), 2006-2025, pour les 12 départements.
- **Variables :** `temperature_2m_max`, `temperature_2m_mean`, `precipitation_sum`, `wind_speed_10m_max`, `wind_gusts_10m_max`, `relative_humidity_2m_min`, `et0_fao_evapotranspiration`, `soil_moisture_0_to_7cm_mean`.
- **Pourquoi elle est essentielle :** ce sont les variables explicatives du modèle de prédiction (sécheresse cumulée, chaleur, vent). Elle couvre toute la période des feux sans clé ni téléchargement lourd, et contient les mêmes ingrédients que l'indice forêt-météo.
- **Limite :** un seul point est grossier pour la Gironde et les Landes.
- **Licence :** les données sont sous CC BY 4.0 ; l'API gratuite est réservée à un usage non commercial, avec des plafonds d'appels. La mention « Weather data by Open-Meteo.com » avec un lien est demandée là où les données sont affichées.

## 5. NASA FIRMS, points chauds MODIS et VIIRS
- **Lien :** https://firms.modaps.eosdis.nasa.gov/api/area/. Une clé gratuite (`FIRMS_MAP_KEY`) est nécessaire.
- **Requête :** `/api/area/csv/{clé}/{source}/-1.8,42.75,2.65,47.2/5/{date}`, par tranches de 5 jours. Sources : `VIIRS_SNPP_SP` (depuis 2012, 375 m) et `MODIS_SP` (depuis 2000, 1 km).
- **Fichiers :** `data/firms/<source>_<année>.csv`.
- **Pourquoi elle est essentielle :** c'est la seule source de **détection** du projet. Elle situe un feu en position, date et heure indépendamment de l'alerte, ce qui permet de mesurer le délai entre détection et alerte.
- **Limite :** FIRMS détecte aussi les brûlages agricoles et les sites industriels. Il faut filtrer sur la confiance et croiser avec la BDIFF.
- **Licence :** NASA soutient le partage ouvert et complet des données ; à toute transmission à un tiers, il faut une mention qui cite FIRMS (https://earthdata.nasa.gov/firms) et LANCE.

---

## Sources écartées

Ces sources ont été étudiées puis retirées pour garder un modèle simple, centré sur la commande. Elles pourront revenir si un besoin précis apparaît.

| Source | Raison de l'écarter |
|---|---|
| Stations Météo-France (données climatologiques quotidiennes) | Redondant avec Open-Meteo : elles servaient seulement à valider la météo modélisée. Fichiers lourds (environ 200 Mo pour la région). |
| Indice forêt-météo (FWI), Copernicus CEMS | Calculé à partir des mêmes variables météo qu'Open-Meteo. Demande un compte Copernicus et des fichiers NetCDF volumineux. Première candidate si l'on veut tester des seuils d'indice avant 2024. |
| Corine Land Cover 2018 | Fichier SIG lourd. Donne une valeur fixe par commune, qui n'apporte rien à un modèle département × jour. |
| BD Forêt V2 (IGN) | Même raison, et redondant avec Corine Land Cover. Téléchargement manuel par département. |
| SIM2, EFFIS, zonage météo, table de passage des communes INSEE, BD TOPO | Repérées mais jamais branchées : apport secondaire pour les questions de la commande. |

Les fichiers déjà téléchargés pour une source écartée (par exemple `data/meteofrance/`) ne sont plus lus par le notebook ni par le pipeline. Ils peuvent être supprimés.

## Données internes du SDIS 33 (hors open data)
À demander au commanditaire. Ce ne sont pas des sources du modèle, mais elles sont indispensables pour chiffrer un seuil en euros et affecter les moyens :
- le seuil de déclenchement actuel ;
- le contenu et le coût journalier du dispositif renforcé ;
- la possibilité de le déclencher par secteur ;
- l'implantation des CIS et des tours de guet ;
- la confirmation que la BDIFF 2024 est complète.

Si ces données contiennent des informations personnelles (agents, victimes), elles seront agrégées avant d'entrer dans la couche silver, et ne seront pas versées dans Git.
