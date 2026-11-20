# Fiche d’identité des archives de la Météo des forêts

**Auteur :** Ahmed ABBADI  
**Territoire de travail :** Gironde et Nouvelle-Aquitaine  
**Consultation et contrôle des fichiers :** 20 novembre 2026  
**Analyse de référence :** [commande Ahmed ABBADI](../analyse/commande-ahmed-abbadi.md), version du dépôt consultée le 20 novembre 2026. Les cinq questions portent sur les zones, les périodes, la relation danger-feux, le seuil compatible avec les moyens et la comparaison territoriale.

Cette source est retenue pour étudier les annonces de danger. Elle doit être rapprochée des incendies observés pour répondre aux questions sur le seuil de renforcement. Les trois archives annuelles disponibles ont été téléchargées, décompressées et lues intégralement.

Cette contribution complète la [fiche partagée du groupe](fiche-meteo-des-forets.md) par un contrôle indépendant et daté. Les volumes du groupe et ceux de l’extrait contrôlé ci-dessous ne doivent pas être confondus.

## Fiche d’identité

| Rubrique | Valeur vérifiée et limites |
| --- | --- |
| Propriétaire et système | Producteur et diffuseur : **Météo-France**. Catalogue sur data.gouv.fr, archives sur le stockage public Météo-France. Identifiant du jeu : `692f01d38fef6c5815d9262a`. La propriété juridique détaillée n’a pas été examinée au-delà du producteur et de la licence déclarés. [S1, S2] |
| Mode d’accès et format | **Téléchargement direct, sans compte**, des archives 2024, 2025 et 2026. Fichiers `.csv.gz`, compression GZIP, texte UTF-8, 5 colonnes. Séparateur **virgule en 2024 et 2025**, **point-virgule en 2026**. L’API de la fiche catalogue fournit des métadonnées ; elle ne doit pas être confondue avec l’API du flux temps réel. [S2, F1 à F3] |
| Grain une ligne représente | **Un département et un horodatage `date`**, avec deux colonnes de danger `niveau_j1` et `niveau_j2`. Le couple département-horodatage est unique dans les 35 616 lignes inspectées. La documentation décrit une production pour J+1 et J+2. La correspondance formelle entre le champ livré `date` et le champ documentaire `Reference_time` est **non vérifiée** : les noms diffèrent. [F1 à F3, S3] |
| Emprise géographique | **96 codes départementaux** présents dans chaque archive, dont `33`, `2A` et `2B`. Les **12 départements de Nouvelle-Aquitaine** sont présents dans chacun des trois fichiers. Aucun code de département d’outre-mer n’est présent dans ces fichiers. [F1 à F3] |
| Période réellement couverte | Horodatages observés du **3 juin au 30 septembre 2024**, du **3 juin au 30 septembre 2025**, du **28 mai au 5 octobre 2026**. Ces bornes concernent la colonne `date`, pas une période d’incendies. Les dates de validité exactes après conversion J+1/J+2 sont **non vérifiées** tant que la sémantique précise de `date` n’est pas confirmée. [F1 à F3] |
| Date de dernière mise à jour affichée sur la fiche | **5 octobre 2026**. Le champ `last_update` de l’API catalogue est `2026-10-05T15:15:29+00:00`. Cette mise à jour ne signifie pas que les données couvrent toute l’année 2026. [S1, S2] |
| Fréquence de mise à jour | **Quotidienne** selon le catalogue ; production saisonnière selon la documentation. Les fichiers inspectés contiennent une ligne par département et par jour entre leurs bornes. Le catalogue affiche également une alerte sur le respect de la fréquence ; aucune publication hors saison n’est supposée. [S1 à S3, F1 à F3] |
| Volumétrie | **35 616 lignes et 5 colonnes** sur les trois archives, hors en-têtes ; **371 lignes pour la Gironde**, **4 452 pour la Nouvelle-Aquitaine**. Détail des tailles compressées, décompressées et des lignes par année ci-dessous. Il s’agit de volumes effectivement mesurés. [F1 à F3] |
| Clés disponibles | Champs réels : `date`, `num_dep`, `niveau_j1`, `niveau_j2` et `nom_dep` ou `dep_nom`. **Clé vérifiée sur ces fichiers : `num_dep` normalisé + `date`.** Conserver les départements comme du texte, ajouter le zéro initial aux codes numériques courts et préserver `2A`/`2B`. Pour une jointure aux feux : département + date de validité + échéance, après confirmation du sens de `date`. [F1 à F3] |
| Données personnelles | Les 5 champs de ces trois fichiers ne contiennent **aucun nom de personne, adresse individuelle, téléphone ou identifiant de personne**. Le nom de département est une information territoriale. Ce constat porte sur les archives inspectées, pas sur tous les systèmes de Météo-France. [F1 à F3] |
| Licence | **Licence Ouverte / Open Licence version 2.0**, code `lov2` dans le catalogue. Citer Météo-France et la date de récupération lors de la réutilisation. [S1, S2] |
| Questions de l’analyse auxquelles elle pourrait répondre | **Le danger annoncé correspond-il à une fréquence plus élevée de feux**, **quel seuil choisir** et **la situation est-elle différente ailleurs** : après jointure aux événements BDIFF de même période. Elle apporte le nombre de jours potentiellement renforcés, mais aucun coût, effectif ou budget. Elle ne localise pas le danger à l’échelle des communes pour **où concentrer les moyens**. |

## Fichiers effectivement inspectés

| Archive | Lignes hors en-tête | Gironde | Nouvelle-Aquitaine | Départements | Octets GZIP | Octets CSV décompressé | Horodatages extrêmes du champ date |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2024 | 11520 | 120 | 1440 | 96 | 40309 | 451602 | `2024-06-03T16:00:00Z` à `2024-09-30T16:00:00Z` |
| 2025 | 11520 | 120 | 1440 | 96 | 43511 | 451602 | `2025-06-03T14:50:06Z` à `2025-09-30T14:50:03Z` |
| 2026 | 12576 | 131 | 1572 | 96 | 49870 | 481597 | `2026-05-28T14:50:07Z` à `2026-10-05T14:50:04Z` |

## Ce que l’ouverture des fichiers a révélé

- Les noms réels sont `date` et `num_dep`, alors que la documentation consultée présente notamment `Reference_time` et `dep_code`. Le pipeline doit partir des en-têtes livrés et faire confirmer la correspondance sémantique.
- Le nom du département est `nom_dep` en 2024 et 2026, mais **`dep_nom` en 2025**.
- Les codes inférieurs à 10 sont écrits sans zéro initial en 2024 et 2025, avec zéro en 2026. Une normalisation textuelle est nécessaire avant concaténation ou jointure.
- Le fichier 2024 n’est pas entièrement trié par date : le bulletin du 3 juin apparaît en fin de fichier. Les bornes ont été calculées sur toutes les lignes, pas déduites de la première et de la dernière ligne.
- Aucun champ vide ni doublon département-horodatage n’a été trouvé dans ces trois archives. Aucun jour intermédiaire ne manque pour la Gironde. Cela ne prouve pas que toutes les révisions intrajournalières ont été archivées : **exhaustivité des versions non vérifiée**.
- Les horaires portent le suffixe `Z`, donc UTC. Le fuseau et le sens des heures d’alerte BDIFF doivent être clarifiés avant rapprochement. Le champ `date` ne doit pas être joint directement à la date d’un incendie sans traiter l’échéance.
- La Météo des forêts est une information départementale destinée au public. L’archive ne contient ni l’IFM détaillé, ni les bulletins professionnels effectivement reçus par le SDIS. [S4]

## Décision pour le projet

**Source retenue**, volume compatible avec le projet. Les fichiers couvrent la Gironde et les comparaisons régionales et nationales métropolitaines. Avant toute mesure de performance, confirmer le sens du champ `date`, choisir une échéance unique et documenter la période commune avec la BDIFF. Aucun seuil opérationnel n’est validé par cette seule exploration.

## Références et traçabilité

- [S1 - Fiche catalogue officielle](https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets).
- [S2 - Métadonnées officielles en JSON](https://www.data.gouv.fr/api/1/datasets/archives-de-la-meteo-des-forets/).
- [S3 - Documentation Météo-France des données expertisées](https://confluence-meteofrance.atlassian.net/wiki/spaces/OpenDataMeteoFrance/pages/874741792/Donn%2Bes%2Bexpertis%2Bes).
- [S4 - Présentation et distinction avec l’assistance aux secours](https://meteofrance.com/actualites/la-meteo-des-forets-sinformer-sur-le-danger-de-feux).
- [F1 - Archive 2024 inspectée](https://meteofrance.s3.sbg.io.cloud.ovh.net/data/BULLETIN/MDF/mdf_2024.csv.gz).
- [F2 - Archive 2025 inspectée](https://meteofrance.s3.sbg.io.cloud.ovh.net/data/BULLETIN/MDF/mdf_2025.csv.gz).
- [F3 - Archive 2026 inspectée](https://meteofrance.s3.sbg.io.cloud.ovh.net/data/BULLETIN/MDF/mdf_2026.csv.gz).

Empreintes SHA-256 des fichiers GZIP récupérés le 20 novembre 2026 :

- `2024` : `e3f87c1161d30491ec7ad1149e0f8b5b89f3974d34dd3200ecbdd1d41b55115f`.
- `2025` : `dd0a095b1744ef7c64e44c3a4560bdbd75a1fcbd7292942ba539c85b79e9e3b0`.
- `2026` : `c02f4f539370a663e290c0dce57c2dc6857a47cfee60b052d4a77ea3cbabf33f`.
