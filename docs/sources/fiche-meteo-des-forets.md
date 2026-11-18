# Fiche source : Archives de la Météo des forêts

**Source n° 2 du projet** (indice à évaluer) · fiche établie le 18/11/2026 à partir des trois archives `data/brut/meteo_des_forets/*.csv.gz`, des fichiers `data/meteo_foret_france.csv` et `data/meteo_foret_na.csv`, et de la fiche data.gouv.fr.

| Rubrique | Valeur |
|---|---|
| **Propriétaire et système** | Météo-France, producteur indiqué sur la fiche data.gouv.fr « Archives de la Météo des forêts » (https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets). Les données sont publiées sur la plateforme data.gouv.fr. |
| **Mode d'accès et format** | Téléchargement sans clé : 3 fichiers principaux au format csv.gz, un par saison, plus 3 fichiers de documentation (zip, geojson, pdf). Script : `python pipeline/telecharger_sources.py --sources mdf`. **Les trois fichiers n'ont pas le même format :** séparateur `,` en 2024 et 2025 mais `;` en 2026 ; libellé du département dans `nom_dep` en 2024 et 2026 mais `dep_nom` en 2025 ; code département « 1 » en 2024 et 2025 mais « 01 » en 2026. Le script harmonise les trois avant d'écrire `meteo_foret_france.csv` et `meteo_foret_na.csv`. |
| **Grain (une ligne = ?)** | Un département × une émission quotidienne, avec deux niveaux : `niveau_j1` (lendemain) et `niveau_j2` (surlendemain). Vérifié : aucun doublon (département, jour d'émission). |
| **Emprise géographique** | France métropolitaine : 96 codes de département, de 01 à 95 plus 2A et 2B. Aucune donnée infra-départementale. Extrait du projet : les 12 départements de Nouvelle-Aquitaine. |
| **Période réellement couverte par les données** | Trois saisons, vérifiées dans les fichiers (dates d'émission) : **du 03/06 au 30/09/2024** (120 jours), **du 03/06 au 30/09/2025** (120 jours) et **du 28/05 au 05/10/2026** (131 jours). Rien hors de ces périodes. |
| **Date de dernière mise à jour affichée sur la fiche** | **5 octobre 2026**, sur la fiche data.gouv.fr consultée le 18/11/2026. Par fichier : 5 octobre 2026, 25 juin 2026 et 24 juin 2026. |
| **Fréquence de mise à jour** | **Non vérifiée :** la fiche ne l'indique pas, et signale même « Fréquence de mise à jour non respectée ». Dans les données, on constate une émission par jour pendant la saison. |
| **Volumétrie** | 3 archives de 451 602, 451 602 et 481 597 octets une fois décompressées. 35 616 lignes France (11 520 + 11 520 + 12 576) × 5 colonnes : `date`, `num_dep`, `niveau_j1`, `niveau_j2`, `nom_dep`. Extrait Nouvelle-Aquitaine : 4 452 lignes (1 440 + 1 440 + 1 572). |
| **Clés disponibles (sur quoi pourra-t-on joindre ?)** | `num_dep`, normalisé sur 2 caractères → `Département` de la BDIFF, `departement` d'Open-Meteo, `departement` des communes. `date` (date d'émission, en UTC) : il faut la ramener au jour local, puis ajouter 1 jour pour `niveau_j1` et 2 jours pour `niveau_j2`, pour obtenir le **jour concerné**. C'est ce jour qui se joint à la date d'alerte de la BDIFF et au jour Open-Meteo. |
| **Données personnelles** | Aucune. Vérifié sur les 5 colonnes : un niveau de danger par département. |
| **Licence** | Licence Ouverte / Open Licence version 2.0, indiquée sur la fiche data.gouv.fr. |
| **Questions de mon analyse auxquelles elle pourrait répondre** | **Q2** (part des jours avec feu pour chaque niveau annoncé, et feux partis en niveau faible ou modéré), avec la BDIFF ; **Q3** (même relation dans les autres départements de la région) ; **Q4** en partie : nombre de jours à danger élevé par département français, grâce au fichier France entière. Questions atomiques : IND-1 à IND-6, TER-1, TER-3. |

## Remarques
- **Heure d'émission différente selon la saison :** 16:00 UTC en 2024 (18 h à Paris), 14:50 UTC en 2025 et 2026 (16 h 50 à Paris). Dans les deux cas, le jour local d'émission est le même que le jour UTC, donc le recalage J+1 / J+2 n'est pas affecté.
- **Répartition des niveaux annoncés pour le lendemain, en Nouvelle-Aquitaine :**

  | Saison | Faible (1) | Modéré (2) | Élevé (3) | Très élevé (4) |
  |---|---|---|---|---|
  | 2024 | 1 335 | 104 | 1 | 0 |
  | 2025 | 1 011 | 351 | 78 | 0 |
  | 2026 | 736 | 645 | 188 | 3 |

  2024 était trop calme pour évaluer un seuil ; 2025 et 2026 apportent les niveaux élevés qui manquaient.
- **Comparaison possible avec les feux : 2024 et 2025 seulement**, car la BDIFF s'arrête au 31/12/2025. En Nouvelle-Aquitaine, la part des jours avec au moins un feu (niveau annoncé la veille) est :

  | Saison | Faible (1) | Modéré (2) | Élevé (3) |
  |---|---|---|---|
  | 2024 | 3,4 % | 13,5 % | 0 %, sur un seul jour |
  | 2025 | 9,4 % | 33,6 % | 43,6 % |

  Les jours de 2026 apparaissent pour l'instant « sans feu » faute de BDIFF 2026 : il ne faut pas les compter comme tels.
- **Hors saison :** aucune donnée avant fin mai ni après début octobre, alors que 35 % des départs girondins ont lieu en dehors de juin à septembre.
