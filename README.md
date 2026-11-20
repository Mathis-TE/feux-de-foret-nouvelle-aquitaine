# feux-de-foret-nouvelle-aquitaine
## Étudiants
Ahmed ABBADI<br>
Amine ASBANE<br>
Mathis TE<br>

## Rendus 
# Data Visualisation
docs/rendus/Rendu Datavisualisation décisionnelle.md



## Bases de Git / GitHub

### Git vs GitHub
- **Git** est l'outil local qui garde l'historique du code. Chaque **commit** est une version enregistrée.
- **GitHub** est le site qui héberge le dépôt en ligne pour que le groupe puisse le partager.

### Commandes de base
| Commande | Rôle |
|---|---|
| `git add <fichier>` | Prépare des modifications pour le prochain commit |
| `git commit -m "message"` | Enregistre une version |
| `git push` | Envoie ses commits sur GitHub |
| `git pull` | Récupère ce que les autres ont envoyé |

### Les branches
- Une **branche** est une ligne de travail parallèle. `main` est la branche principale et doit rester propre et stable.
- Chaque membre du groupe travaille sur **sa propre branche** (par exemple `model`). On peut ainsi modifier ce qu'on veut sans casser le travail des autres.
- `git checkout <nom>` : change de branche.
- `git checkout -b <nom>` : crée une nouvelle branche et s'y place.
- Quand le travail est prêt, on le **fusionne** dans `main`, en général via une **Pull Request** sur GitHub, pour que le groupe puisse relire avant d'intégrer.
- Pour récupérer les nouveautés de `main` dans sa branche : `git pull origin main`.

### Bonnes pratiques
- Faire des petits commits fréquents avec un message clair.
- Faire un `git pull` avant de commencer à travailler, pour limiter les conflits.

### Commande a ne JAMAIS faire
- `git push --force` cette commande détruit le travail déjà présente dans la branche


### Points d'attention
- Ne jamais push sans avoir résolu les conflits de merge
- Ne jamais travailler directement dans la branche main
- Toujours faire un `git pull origin main` pour avoir la dernière version de la main
