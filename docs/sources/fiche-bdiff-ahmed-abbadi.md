# Fiche d’identité de la BDIFF

**Auteur :** Ahmed ABBADI  
**Territoire de travail :** Gironde et Nouvelle-Aquitaine  
**Consultation et contrôle de l’export :** 20 novembre 2026  
**Analyse de référence :** [commande Ahmed ABBADI](../analyse/commande-ahmed-abbadi.md), version du dépôt consultée le 20 novembre 2026. Les cinq questions portent sur les zones, les périodes, la relation danger-feux, le seuil compatible avec les moyens et la comparaison territoriale.

Cette source est retenue pour étudier les incendies déclarés. Un export public a été téléchargé pour la **Gironde, campagnes 2024 et 2025, type de feu F**. Le ZIP, son CSV et les deux PDF joints ont été ouverts. Les constats sur le fichier portent sur cette sélection, pas sur l’intégralité de la base nationale.

Cette contribution complète la [fiche partagée du groupe](fiche-bdiff.md) par un contrôle indépendant et daté. Les volumes du groupe et ceux de l’extrait contrôlé ci-dessous ne doivent pas être confondus.

## Fiche d’identité

| Rubrique | Valeur vérifiée et limites |
| --- | --- |
| Propriétaire et système | **Éditeur : ministère chargé de l’Agriculture** ; conception et développement technique : **IGN** ; hébergement du site chez OVH. Catalogue data.gouv publié par l’IGN. Système : application BDIFF et réseau de contributeurs des services de l’État et des secours. Propriété juridique exhaustive de chaque contribution : **non vérifiée**, non détaillée dans l’export. [S1, S2, PDF des mentions légales] |
| Mode d’accès et format | Consultation publique par formulaire puis **export ZIP**, contenant `Incendies.csv`, `Mention légales.pdf` et `Définitions.pdf`. CSV **UTF-8**, séparateur **point-virgule**, **2 lignes de préambule puis en-tête de 24 colonnes**. La ligne de préambule contient les filtres et le nombre d’incendies. La ressource du catalogue étiquetée « api » pointe vers le portail : aucune API de données garantie n’est déduite de cette étiquette. [S1 à S3, F1] |
| Grain une ligne représente | **Une fiche d’incendie**, et non un appel, une intervention ou un total communal annuel. Clé composite `Année` + `Numéro` : **158 valeurs distinctes sur 158 lignes** dans l’extrait. Le CSV contient la commune et sa référence INSEE, mais **aucune coordonnée de point de départ ni aucun périmètre**. [F1] |
| Emprise géographique | Le portail permet une sélection nationale ou territoriale. **Fichier inspecté : département 33 seulement, 97 codes de commune distincts.** La présence et la complétude de tous les départements de Nouvelle-Aquitaine ou de France dans un export élargi sont **non vérifiées** : ces extractions n’ont pas été réalisées. [S3, F1] |
| Période réellement couverte | Sélection des campagnes **2024 et 2025**. Dates d’alerte réellement présentes : **20 avril 2024 à 16:28:45 au 28 décembre 2025 à 14:49:00**. 2024 : 29 fiches ; 2025 : 129 fiches. Ce sont des bornes d’événements observés, pas une preuve d’absence de feux aux autres dates. Le portail indique **2026 en cours de saisie et non diffusée**. La couverture `2006–2022` du catalogue est ancienne et ne décrit pas cet export. [S1 à S3, F1] |
| Date de dernière mise à jour affichée sur la fiche | **13 décembre 2025** sur la fiche catalogue ; `last_update` vaut `2025-12-13T15:08:54.545000+00:00` dans l’API catalogue. L’autre champ `last_modified` vaut le 11 août 2025. La date de dernière modification de chaque événement est **non vérifiée** : aucune colonne correspondante n’existe dans l’extrait. [S1, S2, F1] |
| Fréquence de mise à jour | **Annuelle** selon le catalogue. La documentation décrit des campagnes annuelles puis une validation de décembre à avril N+1 avant publication. La date de prochain rafraîchissement de l’export et la date définitive de publication de 2026 sont **non vérifiées**. [S2, S4] |
| Volumétrie | ZIP reçu : **596 252 octets**. CSV : **19 102 octets**, **158 lignes de données**, **24 colonnes** ; les 2 préambules et l’en-tête ne sont pas comptés comme événements. Volume total du système national : **non vérifié**, seule la sélection girondine a été téléchargée. [F1] |
| Clés disponibles | `Année` + `Numéro` pour identifier une fiche ; `Département` et `Code INSEE` pour les jointures territoriales ; `Date de première alerte` pour agréger les événements au jour. Clé composite unique et champs de jointure non vides dans cet extrait. Le champ temporel n’a pas de suffixe de fuseau : **fuseau non vérifié** dans le fichier et les définitions jointes. [F1] |
| Données personnelles | Aucun nom de personne, adresse individuelle, téléphone ou identifiant de personne dans les **24 colonnes inspectées**. L’export contient cependant des conséquences par événement, dont des colonnes décès et bâtiments touchés : leur diffusion doit rester adaptée au contexte. Les mentions légales décrivent aussi les comptes utilisateurs, qui ne sont pas les données de ce CSV. Ce contrôle ne certifie pas l’anonymat de toute la base interne. [F1, PDF des mentions légales] |
| Licence | Catalogue data.gouv : **Licence Ouverte 2.0**, code `lov2`. **Incohérence à clarifier** : le PDF des mentions légales livré avec le ZIP, section 7, contient des conditions plus restrictives, notamment sur les usages commerciaux et l’altération des données. Conditions effectives de redistribution **non vérifiées en raison de cette contradiction**. Conserver les références et demander clarification avant diffusion des données brutes. [S1, S2, PDF des mentions légales] |
| Questions de l’analyse auxquelles elle pourrait répondre | **Où concentrer les moyens** : fréquence des fiches au grain communal et surfaces, à compléter par les enjeux et l’accessibilité. **Quand renforcer** : dates/heures d’alerte, pas heure d’éclosion. **Relation danger-feux et seuils** : après jointure aux annonces météo. **Comparaison régionale et nationale** : avec les exports élargis du groupe, dont les contrôles ne sont pas remplacés par cet extrait girondin. La disponibilité des équipes, les coûts additionnels et le budget 2027 ne sont pas renseignés. |

## Contrôles du fichier reçu

| Contrôle | Résultat observé |
| --- | --- |
| Sélection reproduite dans le préambule | Campagnes 2024 et 2025 ; département 33 ; type de feu F ; date limite 31 décembre 2025 à 23:59:00. |
| Répartition des événements | 29 en 2024 ; 129 en 2025 ; 158 au total. |
| Bornes des alertes en 2024 | 20 avril 2024 à 16:28:45 ; 4 octobre 2024 à 22:53:39. |
| Bornes des alertes en 2025 | 19 février 2025 à 18:30:00 ; 28 décembre 2025 à 14:49:00. |
| Identifiants et jointures | 158 couples année-numéro distincts ; 97 communes ; département 33 uniquement ; aucune valeur vide dans année, numéro, département, code INSEE ou date d’alerte. |
| Surfaces | Unité **m²** dans le CSV ; surface totale parcourue **1 436 727 m²**, soit **143,6727 ha** après division par 10 000. Ce total appartient à l’extrait 2024–2025, pas à tous les feux de végétation du SDIS. |
| Précision des surfaces | 154 événements avec surfaces « Estimées » ; 4 avec surfaces « Mesurées ». |
| Causes Nature | 85 cellules vides sur 158. Les cellules vides ne sont pas interprétées comme absence de cause. |
| Colonnes entièrement vides | Plusieurs anciennes catégories de surfaces, le type de peuplement et le champ de précision de la donnée. Une colonne vide ne vaut pas zéro. |
| Conséquences | Le champ « Décès ou bâtiments touchés » est renseigné, mais les trois colonnes de nombres correspondantes ont chacune 132 cellules vides. Ne pas remplacer ces vides automatiquement par zéro. |
| Date de début réel du feu | **Non vérifiée** : le fichier contient une date de première alerte. Selon les définitions jointes, il s’agit de l’arrivée de l’information au CODIS. |

## Limites pour la décision

- Un export de fiches présentes ne certifie pas la couverture des **journées sans événement**. Avant de fabriquer des zéros quotidiens, faire confirmer la complétude des campagnes et le périmètre des feux enregistrés.
- La définition de feu de forêt inclut un incendie qui démarre en forêt ou s’y propage. Le type F exporté ne représente pas nécessairement tous les feux d’herbes, de cultures ou de friches : comparaison avec les catégories SDIS à valider.
- La date d’alerte ne permet pas, seule, de mesurer le délai de détection. L’extrait ne contient ni heure d’éclosion, ni arrivée des engins, ni durée de mobilisation.
- La commune de départ ne donne pas un point précis exploitable pour l’implantation d’un guet ou l’accessibilité d’une piste.
- Les campagnes 2024–2025 sont utilisables pour une exploration jointe aux archives météo après clarification des temps et des définitions. Deux saisons et de petits effectifs ne suffisent pas à garantir un seuil stable pour 2027.

## Décision pour le projet

**Source retenue avec limites explicites.** Elle apporte les dates, les communes et les surfaces indispensables au premier rapprochement avec la Météo des forêts. Pour l’analyse régionale et nationale, il reste à réaliser les mêmes exports et contrôles sur les autres départements. Pour 2026 et les coûts opérationnels, demander des extractions au SDIS 33 et aux services contributeurs.

## Références et traçabilité

- [S1 - Fiche catalogue officielle BDIFF](https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff).
- [S2 - Métadonnées officielles en JSON](https://www.data.gouv.fr/api/1/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff/).
- [S3 - Consultation du portail](https://bdiff.agriculture.gouv.fr/incendies).
- [S4 - Généralités et cycle de validation](https://bdiff.agriculture.gouv.fr/aide/generalites).
- [S5 - Aide sur la recherche et l’export](https://bdiff.agriculture.gouv.fr/aide/recherche).
- [S6 - Définitions du portail](https://bdiff.agriculture.gouv.fr/aide/definitions).
- [S7 - Mentions légales du portail](https://bdiff.agriculture.gouv.fr/mentions-legales).
- [F1 - Sélection Gironde 2024–2025 à reproduire avant export CSV](https://bdiff.agriculture.gouv.fr/incendies?if%5Bdeprts%5D%5Bvalue%5D=33&if%5BperiodeAnnees%5D%5BanneeDeb%5D=2024&if%5BperiodeAnnees%5D%5BanneeFin%5D=2025&if%5Bsubmit%5D=). L’export se récupère ensuite par le bouton CSV dans la même session, à l’adresse `/incendies/zip`. Ce lien d’export dépend de la sélection de la session et ne constitue pas une URL statique de fichier filtré.

Deux pièces de documentation ont été lues dans le ZIP reçu : **Définitions.pdf, 5 pages**, et **Mention légales.pdf, 3 pages**. Leur présence a permis de confirmer le sens de l’alerte et de relever l’incohérence des conditions de réutilisation.

Empreinte SHA-256 du ZIP reçu le 20 novembre 2026 : `076662a3da24ce6f911e7f05bdb8adbbd0cf09f671eb0ab8056cd6e16599d166`.

Empreinte SHA-256 du CSV contenu dans ce ZIP : `ac2a2a9bb145b215f0227c1b4acd7236a09262b873c279ade5dd1ed2f536eddf`.
