# Journal des décisions

**Version :** v0, 20 novembre 2026. **Rédaction :** Ahmed ABBADI. **Statut commun aux entrées :** propositions issues de la confrontation des questions et des fichiers, à relire par le groupe et le ou la responsable sources. Les autres membres sont cités comme auteurs des questions d’origine, pas comme signataires d’un accord.

Références : [matrice v0](sources/matrice.md), [matrice individuelle Ahmed](analyse/commande-ahmed-abbadi.md#5-confronter-mes-questions-aux-sources), [inventaire](sources/inventaire.md), [contrôle des fichiers](sources/verification/confrontation-exercice-3-2026-11-20.json).

<a id="d01-completer-le-diagnostic-spatial"></a>

## D01 Compléter le diagnostic spatial

- **Question :** G01 ; origines AA-Q1, partie spatiale MT-Q1 et diagnostic préalable AS-Q2.
- **Manque :** BDIFF situe les fiches à la commune ; ni surface forestière de référence, ni points de départ précis, accès praticables, points d’eau ou enjeux détaillés dans les quatre sources de l’inventaire.
- **Décision proposée : collecter.** Chercher un référentiel forestier daté et les couches opérationnelles auprès du SDIS/GIP ATGeRi. En attendant, **approximer** la priorité par le classement communal des fiches enregistrées et des surfaces parcourues, sans prétendre optimiser l’implantation des moyens.
- **Raison :** le nombre brut de feux dépend aussi de l’étendue et du contexte des espaces exposés. Le centre d’une commune n’est pas le point d’éclosion. La `surface_ha` communale ne doit pas être remplacée silencieusement par une surface forestière.
- **Ce que cela coûte :** recherche d’accès, contrôle des millésimes et traitement SIG ; délai et coût financier non chiffrés. Le repli communal perd la précision à l’intérieur d’une commune.
- **Date et auteur :** 20 novembre 2026, Ahmed ABBADI ; validation collective en attente.

<a id="d02-utiliser-les-alertes-comme-proxy-temporel"></a>

## D02 Utiliser les alertes comme proxy temporel

- **Question :** G02 et AA-Q2 ; partie temporelle MT-Q1.
- **Manque :** heure réelle d’éclosion. `Date de première alerte` décrit la réception au CODIS selon les définitions BDIFF.
- **Décision proposée : approximer.** Présenter les mois, jours et créneaux des **alertes enregistrées**. Si la précision sur l’éclosion est indispensable, collecter auprès du SDIS une heure estimée accompagnée d’un indicateur de fiabilité.
- **Raison :** conserver l’information disponible sans présenter l’heure d’alerte comme l’heure de départ réelle. Confirmer aussi son fuseau avant les calculs horaires.
- **Ce que cela coûte :** contrôle du fuseau et adaptation des libellés ; collecte SDIS supplémentaire si l’éclosion doit être étudiée. Le proxy peut déplacer les pics horaires.
- **Date et auteur :** 20 novembre 2026, Ahmed ABBADI ; validation collective en attente.

<a id="d03-confirmer-les-temps-et-la-completude-avant-appariement"></a>

## D03 Confirmer les temps et la complétude avant appariement

- **Question :** G03, G04, AA-Q3 et partie descriptive AA-Q4 ; MT-Q2.
- **Manque :** confirmation du sens de `date` dans le schéma livré, fuseau des alertes, gestion des révisions et couverture des jours sans fiche BDIFF.
- **Décision proposée : collecter.** Faire confirmer ces informations par la documentation précise ou le producteur avant le calcul. Fixer une échéance commune, proposée à **J+1**, et un croisement public initial sur **2024–2025**. Aucun zéro ne sera fabriqué tant que la couverture correspondante n’est pas établie.
- **Raison :** comparer ce qui était annoncé avant la décision à ce qui est enregistré ensuite. Les noms documentaires `Reference_time` et `dep_code` diffèrent des en-têtes livrés `date` et `num_dep`. Un danger élevé sans événement ne prouve pas une mauvaise annonce, et ne suffit pas à relever le seuil.
- **Ce que cela coûte :** temps de clarification, construction d’un calendrier de couverture et contrôle des jointures. Sans réponse, les taux de journées avec feu restent non validés et les données inconnues sont conservées comme telles.
- **Date et auteur :** 20 novembre 2026, Ahmed ABBADI ; validation collective en attente.

<a id="d04-collecter-les-couts-et-les-capacites-operationnelles"></a>

## D04 Collecter les coûts et les capacités opérationnelles

- **Question :** G07, G04 et AA-Q4 ; besoins de moyens d’Ahmed et de Mathis.
- **Manque :** seuil actuel, contenu et coût additionnel du dispositif, agents et engins disponibles, durée, zones, contraintes de repos, simultanéité et budget affectable en 2027.
- **Décision proposée : collecter.** Demander ces éléments au SDIS. Sans accès dans le délai, **approximer** uniquement la charge par le nombre de jours à renforcer et les événements historiquement sous le seuil ; **renoncer** à déclarer un seuil optimal en euros ou un nombre de feux évités.
- **Raison :** les comptes annuels OFGL et les statistiques annuelles SIS présents dans le dépôt ne décrivent pas le coût marginal d’une patrouille ni une disponibilité quotidienne. Une simulation descriptive n’est pas une mesure causale de l’efficacité des patrouilles.
- **Ce que cela coûte :** extraction et validation métier par le SDIS, avec délai non garanti ; calculs de scénarios une fois les contraintes connues. Le repli perd la conclusion de faisabilité financière.
- **Date et auteur :** 20 novembre 2026, Ahmed ABBADI ; validation collective en attente.

<a id="d05-retablir-la-comparaison-sur-une-emprise-commune"></a>

## D05 Rétablir la comparaison sur une emprise commune

- **Question :** G05, G06 et AA-Q5 ; MT-Q3 et MT-Q4.
- **Manque :** fichier météo national reproductible dans le dépôt ; validation des campagnes comparées, catégories et éventuels dénominateurs forestiers.
- **Décision proposée : collecter.** Produire et contrôler l’extrait national depuis les trois archives repérées, puis comparer la même période, la même échéance et les mêmes événements. **Approximer le périmètre national** par la couverture commune Hexagone et Corse, en le nommant explicitement. Le volet régional garde les 12 départements.
- **Raison :** `data/meteo_foret_na.csv` ne couvre que la région ; le fichier national annoncé est absent du checkout. BDIFF contient aussi des départements ultramarins, hors de la couverture météo. Les nombres de feux doivent être rapportés aux jours documentés de chaque niveau ; les petits effectifs sont affichés.
- **Ce que cela coûte :** téléchargement, harmonisation, contrôle des campagnes et traitement des dénominateurs. Le périmètre commun exclut l’outre-mer. Une relation statistique semblable n’impose pas à elle seule un seuil régional commun ni un budget identique.
- **Date et auteur :** 20 novembre 2026, Ahmed ABBADI ; validation collective en attente.

<a id="d06-obtenir-la-campagne-2026-sans-fabriquer-de-zeros"></a>

## D06 Obtenir la campagne 2026 sans fabriquer de zéros

- **Question :** scénarios 2027, G01 à G07 ; besoins 2026 de Mathis et hypothèse de charge demandée par le commanditaire.
- **Manque :** événements BDIFF 2026 et mobilisations consolidées de cette campagne, alors que les annonces météo 2026 sont présentes.
- **Décision proposée : collecter.** Demander un extrait provisoire SDIS/DDTM, daté et accompagné de son état de validation. À défaut, **renoncer** à une évaluation danger–feux de 2026 et présenter 2024–2025 comme période historique commune ; conserver 2026 uniquement pour décrire les annonces disponibles.
- **Raison :** une campagne non diffusée n’est pas une campagne sans feu. L’hypothèse « autant de feux qu’en 2026, voire davantage » est un scénario de préparation, pas une prévision démontrée par les sources.
- **Ce que cela coûte :** demande et rapprochement des catégories avec la BDIFF, attente de validation. Le repli réduit la période commune et laisse davantage d’incertitude pour 2027.
- **Date et auteur :** 20 novembre 2026, Ahmed ABBADI ; validation collective en attente.

<a id="d07-encadrer-la-question-de-prevision-et-dia"></a>

## D07 Encadrer la question de prévision et d’IA

- **Question :** G08 ; AS-Q2 et AS-Q3.
- **Manque :** caractéristiques fines des combustibles, du relief, des accès et habitations, prédictions de référence, informations disponibles avant décision et protocole de test. Les quatre sources ne démontrent aucun gain d’un modèle d’IA.
- **Décision proposée : renoncer en v0 à une promesse de prévision opérationnelle à la maille et au jour.** Proposer au groupe un éventuel prototype au département-jour comparé à une règle simple, seulement après contrôle des données et séparation temporelle apprentissage/test. Collecter des données fines si la demande à la maille est maintenue.
- **Raison :** une météo passée reconstruite avec le modèle `best match` ne peut pas être traitée comme une prévision réellement reçue. Un point météo par département et un centre communal ne restituent pas toutes les différences à l’intérieur d’un massif.
- **Ce que cela coûte :** perte de précision spatiale dans le repli ; travail de validation supplémentaire pour un prototype ; données et temps d’étude supplémentaires pour la cible fine. Aucun gain ni budget de développement n’est chiffré à ce stade.
- **Date et auteur :** 20 novembre 2026, Ahmed ABBADI ; extension proposée par Amine, arbitrage collectif en attente.

<a id="d08-separer-evolution-descriptive-et-attribution-climatique"></a>

## D08 Séparer évolution descriptive et attribution climatique

- **Question :** G09 ; AS-Q1.
- **Manque :** séries climatiques longues et homogènes, stabilité des déclarations de feux et variables permettant une attribution causale. La surface parcourue ne mesure pas l’intensité physique du feu.
- **Décision proposée : renoncer à conclure causalement dans cette v0.** Reformuler en comparaison descriptive de l’évolution des événements, des surfaces et des conditions météo sur une période commune. Collecter des séries plus longues et homogènes si l’attribution climatique devient un objectif retenu.
- **Raison :** l’historique feu local est 2006–2025 ; la réponse Open-Meteo contrôlée couvre aussi 2006–2025 sans modèle unique fixé par la requête. Les annonces météo ne couvrent que trois saisons. Une corrélation ne démontre ni causalité ni charge exacte de l’été 2027.
- **Ce que cela coûte :** abandon de la réponse causale et de la projection à long terme dans le rendu initial ; collecte et expertise supplémentaires si elles sont maintenues. Les données descriptives ne permettent pas de fixer seules le budget futur.
- **Date et auteur :** 20 novembre 2026, Ahmed ABBADI ; extension proposée par Amine, arbitrage collectif en attente.

<a id="d09-documenter-les-divergences-entre-fiches-et-fichiers"></a>

## D09 Documenter les divergences entre fiches et fichiers

- **Question :** reproductibilité des G01 à G09 et choix des cellules de couverture.
- **Manque :** concordance entre certains descriptifs historiques et le contenu actuel du dépôt.
- **Décision proposée : collecter les métadonnées exactes et consigner le retour aux fichiers.** Le [rapport de contrôle](sources/verification/confrontation-exercice-3-2026-11-20.json) est produit pour cette confrontation ; la mise à jour des fiches partagées et du pipeline est à faire relire séparément.
- **Raison :** le CSV météo régional fait 4 452 lignes et **6 colonnes**, avec deux alias du nom départemental ; les trois saisons sont présentes. Les archives brutes font 5 colonnes et le fichier national n’est pas dans le dépôt. Le CSV BDIFF du sous-dossier est national 2025, tandis que le fichier concaténé couvre 2006–2025. Les coordonnées, unités, fuseau et modèle renvoyés par Open-Meteo ne sont pas conservés dans le CSV transformé.
- **Ce que cela coûte :** temps de vérification et de documentation, puis réconciliation du pipeline avant utilisation des noms de colonnes ou des métadonnées supposées. Aucun fichier de données ni résultat existant n’est corrigé par la présente confrontation.
- **Date et auteur :** 20 novembre 2026, Ahmed ABBADI ; validation collective en attente.

<a id="d10-fixer-le-perimetre-des-sources-et-lire-la-matrice-dans-les-deux-sens"></a>

## D10 Fixer le périmètre des sources et lire la matrice dans les deux sens

- **Question :** choix des questions retenues et sources utiles, notamment G08 et G09.
- **Manque :** cohérence entre l’inventaire de quatre sources, l’ancienne présentation incluant FIRMS et les sources de contexte stockées sans fiche dans l’inventaire.
- **Décision proposée : renoncer à ajouter une source non explorée dans cette matrice.** Garder les **quatre colonnes de l’inventaire**. Traiter OFGL et interventions SIS comme sources de contexte à documenter si elles entrent dans une question. FIRMS reste écartée conformément au modèle UML existant, à confirmer lors de la réconciliation des documents.
- **Raison :** API Géo et Open-Meteo sont absents des variables directement demandées par les cinq questions individuelles d’Ahmed, mais ils servent les besoins territoriaux et les extensions d’Amine. Cela justifie de discuter les questions, pas de déclarer artificiellement toutes les sources « partielles ». G08 et G09 sont des propositions à arbitrer, pas des questions ajoutées pour conserver une source à tout prix.
- **Ce que cela coûte :** discussion de périmètre, fiches supplémentaires si les sources de contexte sont retenues, et mise à jour documentaire. La v0 n’inclut ni détection satellite ni preuve de gain d’une IA.
- **Date et auteur :** 20 novembre 2026, Ahmed ABBADI ; validation collective en attente.

## Suivi pour le FOAD 1

Lors de la mise en commun, valider ou amender chaque proposition, consigner la date et les personnes qui ont réellement arbitré, affecter les collectes et vérifier les réponses avant tout calcul. Une décision en attente ne devient pas validée par l’écoulement du délai. La PR permet la relecture ; elle ne constitue pas une validation métier du dispositif renforcé.
