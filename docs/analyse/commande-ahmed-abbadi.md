# Partie B — Analyse de la commande

**Nom :** Ahmed ABBADI  
**Région :** Nouvelle-Aquitaine  
**Commanditaire :** SDIS 33 — Gironde

## 1. Questions

Pour commencer, j’ai besoin de préciser certains points de la commande :

- Quels moyens humains et financiers sont disponibles ?
- Que comprend le dispositif renforcé ?
- Quel est le seuil utilisé actuellement ?
- Sur quoi repose l’hypothèse d’une augmentation des feux en 2027 ?
- Quel est l’objectif principal : éviter les départs, intervenir plus rapidement ou limiter les dégâts ?

Ensuite, les questions suivantes peuvent aider la direction à prendre ses décisions :

| Question | Décision possible |
|---|---|
| Dans quelles zones de Gironde y a-t-il le plus de départs de feu ? | Concentrer davantage les patrouilles dans ces zones. |
| À quelles périodes les départs de feu sont-ils les plus fréquents ? | Renforcer les équipes pendant les périodes concernées. |
| Les jours où le danger annoncé est élevé présentent-ils davantage de feux ? | Évaluer si le niveau annoncé aide à décider du renforcement. |
| Selon le seuil choisi, combien de jours faudrait-il renforcer et combien de feux surviendraient sous ce seuil ? | Comparer plusieurs seuils en tenant compte du budget. |
| Observe-t-on la même relation entre danger annoncé et feux dans les autres départements de la région et en France ? | Vérifier si la Gironde nécessite une règle particulière. |

## 2. Termes inconnus ou à préciser

Ces premières définitions restent à vérifier.

| Terme | Première compréhension |
|---|---|
| SDIS | Service départemental d’incendie et de secours. |
| Météo des forêts | Information qui annonce un niveau de danger de feux de forêt. |
| Indice | Indicateur mentionné dans la commande ; il faut préciser lequel est utilisé. |
| Guet | Surveillance permettant de repérer les départs de feu. |
| Dispositif renforcé | Moyens supplémentaires mobilisés, comme des patrouilles ou des équipes. |
| Seuil de déclenchement | Niveau à partir duquel le dispositif renforcé est activé. |
| Chef de centre | Responsable d’un centre d’incendie et de secours. |
| Départ de feu | Début d’un incendie ; les événements à compter doivent être définis. |

## 3. Besoins

Pour répondre à ces questions, j’ai besoin :

- D’un historique des départs de feu avec leurs dates et leurs localisations.
- Des niveaux de danger annoncés pour les mêmes jours.
- Des informations sur les équipes, le matériel et le budget disponibles.
- Du coût et du contenu du dispositif renforcé.
- De données comparables pour la Gironde, la Nouvelle-Aquitaine et le territoire national.

Il faudra également vérifier les informations manquantes et éviter de compter plusieurs fois le même feu.

## 4. Données

Le **grain** indique ce que représente une ligne. L’**emprise** correspond au territoire couvert.

| Question | Données nécessaires | Grain | Période souhaitée | Fraîcheur souhaitée | Emprise |
|---|---|---|---|---|---|
| Où concentrer les moyens ? | Localisation et date des départs de feu. | Un feu. | Plusieurs étés récents, dont 2026 si disponible. | Historique mis à jour avant l’analyse. | Gironde. |
| Quand renforcer les équipes ? | Date et heure des départs de feu. | Un feu. | Même période. | Historique mis à jour avant l’analyse. | Gironde. |
| Le danger annoncé correspond-il à une fréquence plus élevée de feux ? | Niveau annoncé et nombre de feux pour chaque jour. | Un département et un jour. | Période commune aux deux données. | Annonce disponible avant la décision ; feux consolidés ensuite. | Gironde. |
| Quel seuil est compatible avec les moyens disponibles ? | Niveau annoncé, feux observés, coût du renforcement, effectifs et budget. | Un jour et un scénario de renforcement. | Historique récent et prévisions de moyens pour 2027. | Budget et disponibilités à jour. | Gironde. |
| La situation est-elle différente ailleurs ? | Niveaux annoncés et feux observés selon les départements. | Un département et un jour. | Même période pour les départements comparés. | Données mises à jour avant l’analyse. | Nouvelle-Aquitaine et territoire national. |

**À ce stade, je définis les données nécessaires. Leur disponibilité devra être vérifiée lors de la recherche des sources.**


## 5. Confronter mes questions aux sources

**Auteur :** Ahmed ABBADI. **Date :** 20 novembre 2026. Cette section confronte les cinq questions analytiques de la section 1 aux quatre sources de l’[inventaire](../sources/inventaire.md). Les sections 1 à 4 sont conservées sans modification. Les repères `AA-Q1` à `AA-Q5` suivent simplement l’ordre des cinq lignes du tableau initial.

### 5.1 Règle de lecture et preuves

- **complet** : la source couvre les variables, le grain, la période et l’emprise nécessaires à la question telle qu’elle était formulée.
- **partiel** : une partie utile existe, mais une autre variable, période, emprise ou précision manque.
- **absent** : les variables nécessaires à cette question ne sont pas présentes. Une date ou une clé de jointure seule ne suffit pas à rendre une source pertinente.
- **inconnu** : la présence ou le sens d’une information indispensable n’a pas été vérifié. Il faut alors vérifier avant de choisir une autre action.

Une source peut être partielle tout en conservant une métadonnée inconnue : son appariement reste à vérifier avant tout calcul. La couverture est distinguée de la qualité : « complet » ne garantit pas l’exhaustivité des événements enregistrés, ne valide pas une causalité et ne suffit pas à décider de l’affectation des moyens. Les inconnues de complétude et de temps restent des contrôles préalables.

Les preuves utilisées sont les [fiches BDIFF](../sources/fiche-bdiff.md), [contrôles BDIFF Gironde](../sources/fiche-bdiff-ahmed-abbadi.md), [fiche météo](../sources/fiche-meteo-des-forets.md), [contrôles météo](../sources/fiche-meteo-des-forets-ahmed-abbadi.md), [fiche API Géo](../sources/fiche-geo-api-gouv.md), [fiche Open-Meteo](../sources/fiche-open-meteo.md) et le [contrôle des fichiers du dépôt](../sources/verification/confrontation-exercice-3-2026-11-20.json).

### 5.2 Matrice individuelle

| Question initiale | BDIFF | Météo des forêts | API Découpage administratif | Open-Meteo |
| --- | --- | --- | --- | --- |
| **AA-Q1. Dans quelles zones de Gironde y a-t-il le plus de départs de feu ?** | **complet** pour classer les communes selon les feux de forêt enregistrés : `Année`, `Numéro`, `Département`, `Code INSEE`, `Date de première alerte` ; un événement par ligne, 3 555 fiches girondines dans l’historique 2006–2025. La section 4 demandait plusieurs étés et 2026 seulement « si disponible ». Sources : fiche BDIFF, rubriques Grain/Emprise/Période, et contrôle du fichier `data/incendies.csv`. | **absent** : `num_dep` situe un danger au département ; ni événement ni localisation infra-départementale dans les cinq champs des archives. Fiche météo, rubriques Grain et Clés. | **absent** : `code_insee`, `lat`, `lon`, `population` décrivent les communes, sans nombre de feux. Le centre communal n’est pas un départ d’incendie. Fiche Géo, Grain/Clés, et fichier `communes_na.csv`. | **absent** : les huit variables météo et `date` ne contiennent aucun événement d’incendie. Fiche Open-Meteo, Variables disponibles, et fichier `meteo_quotidienne/33.csv`. |
| **AA-Q2. À quelles périodes les départs de feu sont-ils les plus fréquents ?** | **partiel** : `Date de première alerte` permet mois, jour et heure de signalement ; la définition jointe décrit la réception au CODIS, pas l’heure réelle d’éclosion demandée en section 4. Fiche BDIFF, Clés, et notice des définitions. | **absent** : `date` est l’horodatage météo, pas une date de départ de feu ; aucun nombre d’événements. Fiche météo, Grain/Clés. | **absent** : aucun horodatage d’incendie dans `code_insee`, `commune`, `departement`, `lat`, `lon`, `surface_ha`, `population`. Contrôle du fichier communes. | **absent** : `date` décrit un jour de météo historique, sans date ni nombre de départs de feu. Fiche Open-Meteo, Grain/Variables disponibles. |
| **AA-Q3. Les jours où le danger annoncé est élevé présentent-ils davantage de feux ?** | **partiel** : dates et événements dans `Date de première alerte`, `Année`, `Numéro`, mais aucun niveau de danger annoncé. L’absence de fiche ne certifie pas un zéro. Fiche BDIFF, Clés et Limites. | **partiel** : `niveau_j1`, `niveau_j2`, `num_dep`, `date` fournissent l’annonce, sans feux observés. La période commune avec les événements publics est 2024–2025 ; correspondance de `date` avec l’heure de production à confirmer. Fiche météo, Grain/Période/Clés. | **absent** : ni annonce de danger ni nombre d’incendies dans les sept colonnes communales. Contrôle du fichier communes. | **absent** : les températures, la pluie et l’humidité du sol sont des données historiques ; aucune colonne de niveau annoncé de la Météo des forêts ni aucun événement. Fiche Open-Meteo, Variables disponibles. |
| **AA-Q4. Selon le seuil choisi, combien de jours faudrait-il renforcer et combien de feux surviendraient sous ce seuil ?** | **partiel** : les événements peuvent être comptés sous le seuil après jointure ; aucun seuil météo, coût journalier, effectif disponible ou budget 2027 dans les 24 colonnes. La section 4 exige aussi la compatibilité avec les moyens. Fiche BDIFF, Clés/Questions couvertes. | **partiel** : `niveau_j1` ou `niveau_j2` permet les jours à renforcer pour chaque seuil ; aucun événement, coût, disponibilité ou budget. Fiche météo, Clés/Questions couvertes. | **absent** : aucune donnée de seuil, de renforcement, d’effectif ou de coût dans le fichier communes. Fiche Géo, Grain/Clés. | **absent** : aucune donnée de seuil appliqué, de renforcement, de coût ou d’effectif dans les variables météo. Fiche Open-Meteo, Variables disponibles. |
| **AA-Q5. Observe-t-on la même relation entre danger annoncé et feux dans les autres départements de la région et en France ?** | **partiel** : `Département`, `Date de première alerte`, `Année`, `Numéro` permettent des comptages départementaux nationaux ; aucune annonce de danger. La fiche partagée signale des anomalies de complétude à contrôler. Fiche BDIFF, Emprise/Période/Remarques. | **partiel** : les archives contrôlées couvrent 96 départements métropolitains, mais sans événements. Le fichier présent `meteo_foret_na.csv` ne couvre que les 12 départements régionaux ; `meteo_foret_france.csv` est absent du dépôt. Fiches météo, Emprise, et contrôle de présence. | **absent** pour mesurer cette relation : les codes communaux servent de référentiel, sans niveau annoncé ni feu. Fiche Géo, Grain/Clés. | **absent** pour la relation demandée : météo passée, sans niveau annoncé de la Météo des forêts ni événements. Fiche Open-Meteo, Variables disponibles. |

**Bilan de couverture :** 1 cellule « complet », 7 « partiel », 12 « absent ». Aucune présence de variable n’est laissée « inconnu » après contrôle des schémas. Les points encore non vérifiés concernent le sens de certains temps, les conditions de couverture et les règles d’enregistrement : ils sont décrits ci-dessous et ne sont pas assimilés à des données validées.

### 5.3 Décisions pour les questions sans source complète

| Question | Décision | Manque et action | Limite assumée |
| --- | --- | --- | --- |
| AA-Q2 | **approximer** | Utiliser la date et l’heure des premières alertes pour décrire les périodes de signalement. Si l’heure d’éclosion est indispensable, collecter une heure estimée et sa fiabilité auprès du SDIS. [D02](../journal-des-decisions.md#d02-utiliser-les-alertes-comme-proxy-temporel). | Le délai entre éclosion et alerte peut déplacer le profil horaire. Les résultats ne seront pas titrés « heure réelle de départ ». |
| AA-Q3 | **collecter** | Obtenir ou faire confirmer les informations de complétude BDIFF, le fuseau de l’alerte et le sens de `date` dans les archives ; joindre ensuite les sources à une échéance fixée, proposée à J+1, sur 2024–2025. [D03](../journal-des-decisions.md#d03-confirmer-les-temps-et-la-completude-avant-appariement). | Sans validation de couverture, ne pas convertir l’absence de ligne en zéro. Les feux de 2026 manquants ne sont pas des jours sans feu. |
| AA-Q4 | **collecter** | Demander le seuil actuel, le contenu du dispositif, ses coûts additionnels, les effectifs et engins disponibles et l’enveloppe 2027. [D04](../journal-des-decisions.md#d04-collecter-les-couts-et-les-capacites-operationnelles). | À défaut, **approximer** la charge par le nombre de jours à renforcer et les événements sous le seuil ; renoncer à affirmer une compatibilité budgétaire ou un nombre de feux évités. |
| AA-Q5 | **collecter** puis **approximer le périmètre** | Produire et contrôler le fichier météo national à partir des archives déjà repérées ; apparier les mêmes jours et échéances. Restreindre la comparaison au périmètre commun documenté, Hexagone et Corse. [D05](../journal-des-decisions.md#d05-retablir-la-comparaison-sur-une-emprise-commune). | Les résultats ne décriront pas l’outre-mer ni une saison 2026 complète. L’anomalie d’enregistrement de 2024 doit être contrôlée avant classement. |

AA-Q1 dispose d’une couverture technique complète pour un **classement communal des feux de forêt enregistrés**. Il reste à vérifier la complétude des campagnes avant de l’interpréter comme le risque réel. Une implantation précise des patrouilles demande des accès et enjeux complémentaires. La question fusionnée G01 du groupe est donc plus exigeante que AA-Q1 : elle inclut les surfaces forestières et le contexte territorial, ce qui explique sa couverture partielle.

### 5.4 Écarts entre mon besoin initial et les sources

Je souhaitais observer les départs de feu ; je dispose d’abord de fiches enregistrées et de dates d’alerte. Je souhaitais tester un seuil avec les moyens disponibles ; les sources ouvertes documentent des événements et du danger, mais pas les coûts marginaux et les disponibilités. Je souhaitais une comparaison nationale directement reproductible ; le fichier météo local est régional et le fichier national annoncé n’est pas présent.

Le contrôle des fichiers montre aussi que `meteo_foret_na.csv` contient **six colonnes**, avec `nom_dep` et `dep_nom`, tandis que les archives brutes en contiennent cinq. Les 1 440 lignes de 2025 remplissent `dep_nom` et laissent `nom_dep` vide. Le fichier `data/incendies/Incendies.csv` est un export national 2025 de 2 541 fiches : il ne doit être confondu ni avec l’historique `data/incendies.csv` de 52 811 fiches ni avec le contrôle Gironde de 158 événements.

Enfin, l’API Géo et Open-Meteo n’apportent pas directement les variables demandées par mes cinq questions. Leur rôle est discuté dans la [matrice du groupe](../sources/matrice.md) : référentiel et contexte territorial pour la première, météo historique pour les extensions de modélisation et de climat d’Amine. Une réanalyse ne constitue pas l’annonce disponible avant une décision.
