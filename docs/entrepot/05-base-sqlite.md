# Base SQLite : incendies, danger et météo

Cette première base exploitable utilise les CSV déjà présents dans le dépôt. Elle conserve leur provenance et leurs limites. Elle permet l'exploration des incendies en Gironde et en Nouvelle-Aquitaine, avec le périmètre national disponible pour les incendies. Elle ne fournit pas encore un seuil opérationnel validé.

## Construire et vérifier

Depuis la racine du dépôt, avec Python 3.10 ou ultérieur (bibliothèque standard uniquement) :

```sh
python pipeline/construire_base.py
python -m unittest discover -s tests -v
```

La construction produit `data/feux_foret.sqlite` et `data/feux_foret.rapport.json`. Utiliser `--output chemin/base.sqlite` pour choisir un autre emplacement. Une base existante est protégée ; `--replace` demande explicitement sa reconstruction. L'import s'effectue dans un fichier temporaire avant publication : une erreur de données ne remplace pas la base existante.

Ouvrir le fichier avec un client SQLite ou Python. Activer `PRAGMA foreign_keys=ON` sur chaque connexion d'écriture. Les exemples d'analyse sont dans `sql/requetes_analyse.sql` ; le schéma complet est dans `sql/schema_sqlite.sql`.

## Contenu de la première construction

- 52 811 fiches d'incendie, de 2006 à 2025, dont 3 555 en Gironde et 8 947 en Nouvelle-Aquitaine.
- 4 452 bulletins de danger pour les 12 départements de Nouvelle-Aquitaine, de 2024 à 2026 : 8 904 prévisions en séparant J+1 et J+2.
- 87 660 observations météorologiques quotidiennes, de 2006 à 2025, réparties dans 12 fichiers départementaux.
- 4 293 communes de l'extrait fourni, complétées par des références non résolues pour conserver tous les incendies sans inventer leur localisation.
- Quatre tables opérationnelles vides : dispositifs, activations, disponibilité des moyens et budgets. Leur remplissage nécessite les données du SDIS.

`data/incendies.csv` est l'unique entrée incendies. Le fichier annuel 2025 séparé n'est pas ajouté une seconde fois. Les fichiers de contexte financier et d'interventions du dépôt ne sont pas importés dans cette version.

## Traçabilité et contrôles

Les 15 CSV d'entrée sont archivés à l'identique, compressés en gzip dans `import_fichier.contenu_gzip`, avec chemin, empreinte SHA-256, taille, colonnes, séparateur et nombre de lignes. Ce sont les fichiers transformés du projet, pas une certification des données primaires. Les faits conservent leur import et leur numéro de ligne physique. `v_imports` expose les métadonnées sans les archives binaires.

La construction contrôle les doublons, clés étrangères, plages des niveaux de danger, valeurs numériques, correspondances département/fichier, intégrité SQLite et empreintes des archives. Elle conserve les avertissements dans `controle_qualite` et le rapport JSON. Les huit tests vérifient notamment les valeurs manquantes, les dates non validées et la protection d'une base existante.

## Règles d'interprétation

**Un jour sans fiche n'est pas automatiquement un jour sans feu.** `couverture_incendie` reste non vérifiée pour 2006–2025 et hors période importée pour 2026–2027. Dans `v_jour_departement`, un décompte positif signifie des fiches présentes ; un jour sans fiche reste NULL tant que la couverture n'est pas explicitement validée complète, avec auteur, date et justification. Le calendrier jusqu'à fin 2027 facilite les jointures et ne constitue pas une prévision.

L'heure BDIFF est celle de l'alerte, sans fuseau confirmé ; elle ne prouve pas l'heure d'éclosion. Les dates de validité MDF proposées sont une hypothèse fondée sur la date source convertie en Europe/Paris puis décalée de J+1 ou J+2. Elles restent distinctes des dates confirmées. `v_appariement_j1_a_confirmer` est exploratoire ; `v_appariement_j1_valide` exige un alignement validé et une couverture incendies confirmée complète. Elle est initialement vide. Ne pas calculer de taux de fausses alertes sur les jours inconnus.

Les surfaces d'incendie sont conservées en m² et les vues les convertissent explicitement en hectares. Les comptes manquants restent NULL ; le drapeau « Non » des conséquences reste séparé des comptes de victimes ou bâtiments. Les 1 285 fiches signalées partielles ou non valides restent identifiables.

Les coordonnées communales représentent le centre de la commune, jamais le point de départ du feu. Le millésime du référentiel et l'unité déclarée de sa surface ne sont pas confirmés. Les anciens codes ne sont pas remappés sans correspondance officielle.

Les données météo historiques représentent un point par département, pas une moyenne départementale ni une prévision. Les coordonnées exactes, le modèle, le fuseau et les unités attestées ne figurent pas dans les fichiers importés : ces métadonnées restent inconnues. La base ne permet pas une comparaison nationale de la Météo des forêts, absente hors Nouvelle-Aquitaine.

## Compléments nécessaires

Obtenir les archives MDF nationales avec leur documentation temporelle ; confirmer l'exhaustivité BDIFF et récupérer les incendies 2026 ; documenter les points et unités météo ; ajouter les correspondances historiques INSEE officielles ; obtenir les secteurs opérationnels, effectifs, activations et coûts du SDIS. Les coûts sont prévus en centimes entiers. Le choix d'un seuil devra ensuite comparer feux détectés, feux manqués et jours de renforcement, avec validation sur des saisons distinctes.

La divergence relevée entre les métadonnées de licence BDIFF et les mentions du document associé reste à clarifier avant redistribution publique des archives intégrées. Le fichier SQLite contenant ces archives reste une livraison locale ; seuls le code, le schéma, les tests et la documentation sont proposés dans Git.

Références techniques : [clés étrangères SQLite](https://www.sqlite.org/foreignkeys.html), [transactions SQLite](https://www.sqlite.org/lang_transaction.html), [module sqlite3 Python](https://docs.python.org/3/library/sqlite3.html).
