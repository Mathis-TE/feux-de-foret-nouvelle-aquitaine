# Partie B — Analyse de la commande

**Nom :** Amine ASBANE  
**Région :** Nouvelle-Aquitaine  
**Commanditaire :** SDIS 33 — Gironde

## 1. Questions

Pour commencer, j’ai besoin de préciser certains points de la commande :

- Sur quel territoire et sur quelle période porte l’étude ?
- Quels moyens humains, techniques et financiers sont disponibles ?
- Que veut-on prévoir exactement : le nombre de feux, leur intensité, leur surface ou leur localisation ?
- Quel horizon de prévision est visé : le lendemain, la saison, les prochaines décennies ?
- Quel est l’objectif principal : mieux prévenir, mieux intervenir ou mieux anticiper l’avenir ?

Ensuite, les questions suivantes peuvent aider la direction à prendre ses décisions :

| Question | Décision possible |
|---|---|
| Le changement climatique augmente-t-il la fréquence et l’intensité des incendies ? | Décider si la prévention et les moyens doivent être renforcés sur le long terme. |
| Comment peut-on utiliser les données des incendies passés pour prédire les zones à risque dans le futur ? | Concentrer la prévention, la surveillance et les équipements dans les zones les plus à risque. |
| Comment l’intelligence artificielle pourrait-elle améliorer la précision de la prévision des incendies ? | Décider s’il est utile d’investir dans un outil de prévision basé sur l’IA, en comparaison des méthodes actuelles. |

## 2. Termes inconnus ou à préciser

Ces premières définitions restent à vérifier.

| Terme | Première compréhension |
|---|---|
| Changement climatique | Évolution durable du climat (température, précipitations, sécheresse) sur plusieurs décennies. |
| Fréquence | Nombre d’incendies observés sur une période donnée. |
| Intensité | Puissance ou gravité d’un incendie ; il faut préciser comment elle est mesurée (surface brûlée, durée, énergie dégagée). |
| Départ de feu / incendie | Début d’un feu ; les événements à compter doivent être définis (seuil de surface, feux de forêt uniquement ou non). |
| Zone à risque | Zone où la probabilité qu’un incendie démarre ou se propage est plus élevée ; il faut distinguer l’aléa (probabilité du feu) et le risque (conséquences possibles). |
| Prévision | Estimation de ce qui peut se produire dans le futur à partir de données. |
| Précision | Capacité d’une prévision à correspondre à ce qui s’est réellement passé ; il faut choisir comment la mesurer. |
| Intelligence artificielle | Méthodes qui apprennent à partir de données pour faire des prédictions (apprentissage automatique). |
| Maille | Petit carré du territoire utilisé pour découper une carte et analyser chaque zone séparément. |

## 3. Besoins

Pour répondre à ces questions, j’ai besoin :

- D’un historique des incendies avec leurs dates, leurs localisations, leurs surfaces et, si possible, leurs causes.
- De données climatiques sur une longue période : températures, précipitations, sécheresse.
- De données sur le territoire : type de végétation, relief, routes, habitations.
- De données météo et d’indices de danger pour comparer avec les feux observés.
- D’informations sur les méthodes de prévision actuelles, afin de comparer leurs résultats avec ceux d’un modèle d’IA.

Il faudra également vérifier les informations manquantes, éviter de compter plusieurs fois le même feu et s’assurer que les données sont comparables dans le temps.

## 4. Données

Le **grain** indique ce que représente une ligne. L’**emprise** correspond au territoire couvert.

| Question | Données nécessaires | Grain | Période souhaitée | Fraîcheur souhaitée | Emprise |
|---|---|---|---|---|---|
| Le changement climatique augmente-t-il la fréquence et l’intensité des incendies ? | Nombre de feux et surfaces brûlées ; températures, précipitations et sécheresse. | Un territoire et une année (ou un mois). | Plusieurs décennies, la plus longue série disponible. | Historique mis à jour avant l’analyse. | Territoire étudié et France pour comparer. |
| Comment utiliser les incendies passés pour prédire les zones à risque ? | Localisation, date, surface et cause des feux ; végétation, relief, routes, habitations. | Un feu ; puis une maille et une période pour la modélisation. | Plusieurs années récentes. | Historique mis à jour avant l’analyse. | Territoire étudié. |
| L’IA peut-elle améliorer la précision de la prévision ? | Feux observés, météo, indices de danger, caractéristiques du territoire, résultats des méthodes actuelles. | Une maille et un jour. | Historique récent, avec une partie gardée de côté pour tester le modèle. | Données quotidiennes, mises à jour régulièrement. | Territoire étudié. |

**À ce stade, je définis les données nécessaires. Leur disponibilité devra être vérifiée lors de la recherche des sources.**
