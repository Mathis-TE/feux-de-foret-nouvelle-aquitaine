# Analyse de la commande - Mathis TE

## 1. Les questions

Quatre questions dont la réponse aiderait la direction à trancher.

> [!test] Test
> Le test : si la réponse est X, la direction fait A ; si elle est Y, elle fait B. Si A et B sont identiques, ce n'est pas une question analytique pertinente.

1. **Quelles communes de Gironde concentrent le plus de départs de feu et le plus de surface brûlée, et à quelles périodes (mois, heures) ?**
   Si les départs sont concentrés sur quelques communes et créneaux, la direction y affecte en priorité patrouilles et guet. S'ils sont diffus sur tout le département, elle investit plutôt dans la détection rapide et la sensibilisation à grande échelle.

2. **Pour chaque niveau de la Météo des forêts, quelle part des jours a connu au moins un départ de feu en Gironde, et combien de feux sont partis des jours classés « faible » ou « modéré » ?**
   Si beaucoup de feux partent dès le niveau « modéré », la direction abaisse le seuil de déclenchement. Si le niveau « élevé » produit surtout des jours sans feu, elle le relève ou ne déclenche qu'en « très élevé », ce qui réduit le nombre de jours de dispositif renforcé à payer.

3. **Un même niveau de danger correspond-il au même nombre de feux en Gironde que dans les autres départements de Nouvelle-Aquitaine (Landes, Lot-et-Garonne, Dordogne…) ?**
   Si c'est le cas, la Gironde peut aligner son seuil sur un seuil régional commun et mutualiser les moyens avec les SDIS voisins. Sinon, elle fixe un seuil propre à son territoire.

4. **Comment se situe la Gironde par rapport aux autres départements français, en nombre de feux et en surface brûlée par jour de danger élevé ?**
   Si la Gironde fait partie des départements les plus touchés, la direction dispose d'un argument pour demander des moyens supplémentaires (État, région) et s'inspirer des seuils des départements comparables. Si elle est dans la moyenne, elle doit travailler à budget constant et cibler plus finement.

## 2. Les termes inconnus

Les mots de la commande que vous ne savez pas définir précisément, ou qui peuvent se comprendre de plusieurs façons.

| Terme | Ce que je crois qu'il veut dire | Ce qu'il faudrait vérifier |
|---|---|---|
| Météo des forêts | Carte publiée chaque jour en saison par Météo-France (depuis 2023), qui donne un niveau de danger de feu par département pour le lendemain et le surlendemain. | La période de publication exacte (juin-septembre ?) et si les archives conservent la prévision J+1, J+2 ou les deux. |
| Niveau / indice | La Météo des forêts a 4 niveaux (faible, modéré, élevé, très élevé), traduction de l'IFM (Indice forêt météo), calculé à partir de la température, de l'humidité, du vent et des pluies. | Les bornes d'IFM de chaque niveau, et si l'IFM brut (valeur numérique) est disponible en open data. |
| Seuil actuel | Le niveau à partir duquel le SDIS 33 active aujourd'hui le dispositif renforcé. | Sa valeur réelle (« élevé » ? « très élevé » ?), demandée au SDIS. |
| Dispositif renforcé | Moyens supplémentaires activés les jours à risque : patrouilles, guet, pré-positionnement d'engins. | Son contenu exact, son coût par jour et s'il peut être déclenché par secteur plutôt que sur tout le département. |
| Guet | Surveillance du massif depuis des tours / vigies pour repérer un départ de feu au plus tôt. | Le nombre et l'emplacement des tours de guet en Gironde. |
| Départ de feu | Le moment où un feu se déclare (éclosion), par opposition à sa propagation. | Si la BDIFF compte tous les départs ou seulement les feux ayant dépassé une certaine surface. |
| Moyens humains comme financiers | Effectifs de pompiers, véhicules, et budget de prévention / lutte. | Le budget disponible pour la saison 2027 et la part déjà engagée. |
| Territoire national | La France entière. | France métropolitaine seule, ou avec la Corse et l'outre-mer ? (la Météo des forêts couvre l'Hexagone et la Corse). |

## 3. Les besoins

La décision à éclairer, en une phrase :

Où concentrer les moyens du SDIS 33 et à partir de quel niveau de la Météo des forêts déclencher le dispositif renforcé pour l'été 2027, avec un budget qui ne permet pas de le déployer partout et tout l'été.

Ce qui manque dans la commande pour y répondre (une information, une précision, une hypothèse à confirmer) :
- Le seuil de déclenchement actuel.
- Le coût d'une journée de dispositif renforcé et le budget total, pour traduire un seuil en euros.
- La priorité de la direction : vaut-il mieux rater un feu ou payer des jours de dispositif inutiles ? C'est ce qui fixe le compromis du seuil.
- Si le dispositif peut être déclenché par secteur (massif, centre de secours) ou seulement sur tout le département.
- Hypothèse à confirmer : l'été 2027 ressemblera à l'été 2026 (comme l'annonce la commande), donc les données récentes sont représentatives.
- Le niveau de comparaison voulu avec la prévision : le feu est-il comparé au niveau annoncé la veille (logique de déclenchement) ou à celui du jour même ?

## 4. Les données

Pour chaque question, la donnée qu'il vous faudrait idéalement pour répondre.

| Question | Donnée idéale | Grain (une ligne = ?) | Période | Fraîcheur | Emprise géographique |
|---|---|---|---|---|---|
| 1 | Feux de forêt avec commune (code INSEE), date et heure de première alerte, surface brûlée et cause (BDIFF), rapportés à la surface forestière de chaque commune (BD Forêt IGN) | Un feu + une commune | 2006-2026 | Annuelle (saison validée) | Gironde, à la commune |
| 2 | Niveau de danger Météo des forêts de chaque jour croisé avec le nombre de feux du même jour (archives Météo des forêts + BDIFF), idéalement complété par l'IFM brut | Un jour × un département | Saisons 2023-2026 (plus long avec l'IFM, dont 2022) | Quotidienne | Gironde |
| 3 | Même croisement niveau de danger × nombre de feux que la question 2 | Un jour × un département | Saisons 2023-2026 | Quotidienne | Les 12 départements de Nouvelle-Aquitaine |
| 4 | Nombre de feux par surface forestière et taux de jours avec feu | Un jour × Un département   | 2023-2026 pour l'indice, 2006-2026 pour les feux | Annuelle | France (Hexagone + Corse) |
