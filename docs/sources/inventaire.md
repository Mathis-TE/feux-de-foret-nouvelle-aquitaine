# Inventaire des sources

**Préparé par :** Ahmed ABBADI  
**Date de mise à jour :** 20 novembre 2026  
**Périmètre :** fiches déjà présentes sur `main` et contrôles complémentaires de la contribution Ahmed ABBADI. Cet inventaire reste à relire lors de la mise en commun du groupe.

| Source | Explorée par | Pertinente pour nos questions | Ce que nous avons découvert |
| --- | --- | --- | --- |
| **BDIFF** — [fiche partagée](fiche-bdiff.md), [contrôle Ahmed](fiche-bdiff-ahmed-abbadi.md) | Mathis-TE pour la fiche existante ; Ahmed ABBADI pour le contrôle complémentaire | Oui : zones et périodes des feux ; relation danger-feux et seuils après jointure ; comparaison territoriale avec les exports du groupe. | La fiche partagée décrit un historique national 2006–2025. Un nouvel export Gironde 2024–2025 a été ouvert : 158 fiches, 24 colonnes et 97 communes. Surfaces en m² ; 85 causes vides ; aucun point de départ géoréférencé. 2026 n’est pas diffusée. Licence ouverte affichée au catalogue et mentions légales jointes plus restrictives : contradiction à clarifier. |
| **Météo des forêts** — [fiche partagée](fiche-meteo-des-forets.md), [contrôle Ahmed](fiche-meteo-des-forets-ahmed-abbadi.md) | Mathis-TE pour la fiche existante ; Ahmed ABBADI pour le contrôle complémentaire | Oui : évaluer le lien entre danger et feux, comparer les seuils en jours à renforcer et comparer les départements. | Trois archives annuelles ouvertes et lues intégralement : 35 616 lignes, 96 départements, 371 lignes pour la Gironde. Séparateurs, noms de colonnes et codes départementaux varient selon les années. Le sens du champ livré `date` doit être confirmé par rapport au schéma de documentation avant de traiter J+1/J+2. |
| **API Découpage administratif** — [fiche Amine](fiche-geo-api-gouv.md) | Amine ASBANE, selon la fiche existante | Oui : rattacher les événements aux communes et départements ; approcher certains enjeux. | La fiche décrit 4 293 communes en Nouvelle-Aquitaine, dont 534 en Gironde. Le référentiel est courant : les anciens codes INSEE des feux peuvent ne plus correspondre aux communes actuelles. Le centre communal ne représente pas un point d’éclosion précis. Les fichiers de cette source n’ont pas été réinspectés dans la présente contribution. |
| **Open-Meteo Historical Weather** — [fiche Amine](fiche-open-meteo.md) | Amine ASBANE, selon la fiche existante | Oui pour expliquer les conditions météo historiques ; complément pour interpréter les contrastes territoriaux. | La fiche décrit une réponse quotidienne 2006–2025 pour un point de Bordeaux, modèle par défaut `best match`. Une réanalyse reconstitue la météo passée ; elle ne remplace pas la prévision reçue avant une décision. Un seul point par département limite la représentation de la Gironde. Les fichiers de cette source n’ont pas été réinspectés dans la présente contribution. |

Les attributions des fiches partagées BDIFF et météo proviennent du commit `f98287fe9151ab54e42f37df4d7db75b239563c2`, publié par le compte Mathis-TE. Les fiches Open-Meteo et API Géo désignent explicitement Amine ASBANE comme auteur. L’inventaire rapporte leurs constats sans les présenter comme de nouveaux contrôles par Ahmed.

## Quelles questions de nos analyses n’ont encore aucune source

Les sources documentées ne renseignent pas les **disponibilités réelles des équipes et véhicules**, les **renforcements effectivement appliqués par zone et créneau**, les **coûts additionnels** d’une patrouille ou du guet, ni le **budget affectable à la saison 2027**. Ces éléments manquent pour répondre complètement à la question du seuil compatible avec les moyens. Les comptes annuels SDIS présents dans le dépôt donnent un contexte financier, sans remplacer ces données opérationnelles.

Pour **où concentrer les moyens**, la fréquence des feux est documentée, mais les accès opérationnels, les points d’eau et les enjeux locaux demandent encore des sources contrôlées. Pour les scénarios fondés sur **2026**, l’accès public BDIFF ne fournit pas cette campagne. Enfin, les jours sans ligne BDIFF ne deviennent pas automatiquement des zéros : la complétude des campagnes doit être confirmée.

## Quelle source nous a surpris et pourquoi

Les archives météo montrent que trois fichiers d’une même source peuvent avoir des schémas différents : `dep_nom` en 2025 contre `nom_dep` les autres années, virgule en 2024–2025 contre point-virgule en 2026, et codes de département avec ou sans zéro initial. L’export BDIFF montre aussi pourquoi il faut ouvrir un fichier : les surfaces sont en m² alors que le tableau du portail les affiche en hectares. Le nombre de lignes de préambule dépend de l’export : **2** dans l’extrait Gironde 2024–2025, **3** dans les anciens exports nationaux décrits par la fiche partagée.

## Quelle source semble utile mais inexploitable dans le temps du projet

La **campagne BDIFF 2026 en accès public** serait essentielle au scénario de référence, mais elle est annoncée en cours de saisie et non diffusée au 20 novembre 2026. Sa publication avant le rendu du 11 décembre n’est pas garantie. Un extrait provisoire SDIS/DDTM est une solution à demander, avec sa date d’arrêté et son état de validation. Les bulletins professionnels et les journaux de renforcement seraient également utiles, mais leur accès et leur exploitabilité dans le délai restent à vérifier.

## Sources complémentaires à répartir

- **Enjeux et végétation :** [Insee à 200 m](https://www.insee.fr/fr/statistiques/8735162?sommaire=8735243), [CoSIA IGN](https://data.geopf.fr/telechargement/resource/COSIA), [acquisitions PIGMA après incendies 2026](https://www.pigma.org/portail/fr/jeux-de-donnees/acquisitions-aeriennes-post-incendie-saumos-et-biscarrosse-2026/info).
- **Accessibilité :** [atlas DFCI du GIP ATGeRi](https://draaf.nouvelle-aquitaine.agriculture.gouv.fr/IMG/pdf/fiche_gipatgeri.pdf), à accès réservé, et informations opérationnelles des centres.
- **Contexte financier :** [comptes des SDIS 2012–2025, OFGL](https://www.data.gouv.fr/datasets/comptes-des-sdis-2012-2025), puis coûts marginaux et moyens du SDIS pour les décisions.
- **Prévention et décision :** archives des bulletins réellement reçus et historique des restrictions préfectorales, distinctes des niveaux de la Météo des forêts.

Ces pistes ne constituent pas de nouvelles fiches explorées. Leur disponibilité et leurs fichiers doivent être vérifiés avant de les intégrer comme sources acquises. La relecture du responsable sources et la décision de fusion dans `main` restent à réaliser.
