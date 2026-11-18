# Fiche source : BDIFF, Base de données des incendies de forêt en France

**Source n° 1 du projet** (cible) · fiche établie le 18/11/2026 à partir des exports `data/incendies2006-2016/Incendies.csv` et `data/incendies2017-2025/Incendies.csv`, de leurs notices (`Définitions.pdf`, `Mention légales.pdf`) et du fichier concaténé `data/incendies.csv`.

| Rubrique | Valeur |
|---|---|
| **Propriétaire et système** | Ministère de l'Agriculture et de la Souveraineté alimentaire (MASA), éditeur du site bdiff.agriculture.gouv.fr. Le traitement relève de la DGPE (sous-direction Filières forêt-bois, cheval et bioéconomie). Conception, développement et hébergement technique : IGN ; serveurs chez OVH. La saisie est faite par des opérateurs dans le cadre de la circulaire interministérielle DGFAR/SDFB/C2006-5016 et du règlement européen n° 1737/2006 (source : `Mention légales.pdf`). |
| **Mode d'accès et format** | Export CSV depuis la recherche du site, sans API. Fichiers en UTF-8, séparateur `;`. Les **3 premières lignes sont des métadonnées** et non des données : un avertissement (« Certaines données sont associées à l'ancienne version du formulaire incendie »), le nombre de fiches et les critères de sélection. L'en-tête des colonnes est en ligne 4. Critères des deux exports : France entière, `Type de feu : F`, alerte du 01/01/2006 au 31/12/2016 et du 01/01/2017 au 31/12/2025. Le notebook concatène les deux exports dans `data/incendies.csv`. |
| **Grain (une ligne = ?)** | Un incendie (une fiche). Clé (`Année`, `Numéro`), vérifiée unique sur les 52 811 fiches. |
| **Emprise géographique** | France entière : 97 codes de département, dont l'outre-mer (971, 972, 974, 976). Le lieu le plus fin est la **commune** (`Code INSEE`) : aucune coordonnée. Dont 8 947 fiches en Nouvelle-Aquitaine et 3 555 en Gironde. |
| **Période réellement couverte par les données** | Alertes du **01/01/2006 12:50 au 31/12/2025 16:22**, vérifié dans le fichier. Trous constatés : aucune fiche pour les Pyrénées-Atlantiques (64) en 2010-2011 ; 2024 anormalement basse en Nouvelle-Aquitaine (98 fiches, contre 353 en 2023 et 484 en 2025), à confirmer. **Aucune donnée 2026** dans les exports. |
| **Date de dernière mise à jour affichée sur la fiche** | **Non vérifiée.** Le site n'autorise pas la lecture automatique (robots) et les exports ne contiennent aucune date de mise à jour. Pour mémoire, les exports ont été téléchargés le 17/11/2026 (11 h 44 et 11 h 50) : c'est une date de téléchargement, pas de mise à jour. |
| **Fréquence de mise à jour** | **Non vérifiée** : ni les exports ni leurs notices (`Définitions.pdf`, `Mention légales.pdf`) ne l'indiquent. |
| **Volumétrie** | 2 exports : 28 251 fiches (2 965 187 octets, 2006-2016) et 24 560 fiches (2 720 228 octets, 2017-2025). Fichier concaténé : 52 811 fiches × 24 colonnes, 5 012 724 octets. |
| **Clés disponibles (sur quoi pourra-t-on joindre ?)** | `Code INSEE` (5 caractères, à lire en texte) → communes (`code_insee`), avec 137 fiches de la région sur des communes fusionnées depuis. `Département` → Météo des forêts (`num_dep`) et Open-Meteo (`departement`). `Date de première alerte` (heure locale), ramenée au jour → jour cible de la Météo des forêts et jour Open-Meteo. (`Année`, `Numéro`) → identifiant du feu, auquel on rattache les détections FIRMS. |
| **Données personnelles** | **Aucune donnée nominative** dans les 24 colonnes (vérifié) : ni nom, ni adresse, ni coordonnées. **Risque indirect :** `Nombre de décès` et la cause `Malveillance`, croisés avec une commune et une date, peuvent renvoyer à un événement connu et aux personnes concernées. On ne diffuse donc pas ces fiches une à une. Les données personnelles décrites dans `Mention légales.pdf` (§3) concernent les comptes utilisateurs du site, pas les fiches incendies. |
| **Licence** | Pas de licence ouverte. Selon `Mention légales.pdf` (§7), la réutilisation est autorisée sans but commercial, à trois conditions : ne pas modifier les données, citer bdiff.agriculture.gouv.fr comme source, et indiquer que les droits de reproduction sont réservés. |
| **Questions de mon analyse auxquelles elle pourrait répondre** | Toutes, car c'est la variable cible : **Q1** (communes et périodes qui concentrent les départs et les surfaces en Gironde) ; **Q2** (part des jours avec feu selon le niveau annoncé), avec la Météo des forêts ; **Q3** (même relation dans les autres départements de la région) ; **Q4** (position de la Gironde parmi les départements français). Questions atomiques : LOC, TEMP, AMP, CAU, TER-2, et toutes les autres par jointure. |

## Remarques
- **Remplissage en Nouvelle-Aquitaine :**
  - colonnes d'identification, de date, de lieu et de surface totale : 100 % ;
  - cause (`Nature`) : 37,8 % seulement, donc 62 % de causes inconnues ;
  - `Précision des surfaces` : 29,4 % ;
  - `Type de peuplement` et surface maquis-garrigues : 0 %, car ces champs ne concernent que l'aire méditerranéenne.
- **Changement de nomenclature :** les catégories de surface changent en 2023 (`Définitions.pdf`). Les anciennes colonnes (avant 2023) et les nouvelles cohabitent, et sont harmonisées dans la couche silver.
- **Cohérence vérifiée :**
  - aucune surface de forêt ne dépasse la surface totale ;
  - aucune date ne sort de l'année déclarée ;
  - le département correspond toujours aux deux premiers caractères du code INSEE.
- **Définition de référence :** un incendie de forêt est un « incendie qui démarre en forêt ou qui se propage en forêt ou au sein de terres boisées au cours de son évolution » ; la date d'alerte est le moment « où l'information d'un départ de feu parvient au CODIS » (`Définitions.pdf`).
