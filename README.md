# FindYourMusic

FindYourMusic est un projet de scraping de 2 sites, Billboard et Genius qui permet via une application Flask de faire une recherche en fonction de l'artiste, le titre de la musique ou les paroles, et de trouver la ou les musiques associées.

## Installation
### Librairies
Voici la liste des librairies utilisés pour ce projet :

* pandas 
* numpy
* flask
* flask_wtf
* plotly
* re
* scrapy
* pymongo
* elasticsearch

On peut les installer en utilisant la commande suivante :
```
pip install "nom de la librairie"
```
## Projet
### Données
Nous avons construit notre base de données en utilisant scrapy, nous avons récupéré la liste des musiques sur https://www.billboard.com/charts/billboard-200 de 2000 à nos jours et les paroles assosiées aux musiques sur https://genius.com/.

### Application
##### Page d'accueil
Sur la page d'accueil on dispose de 4 boutons pour choisir le mode de recherche, par titre, par artiste, par paroles ou un bouton random qui propose une musique aléatoire.
##### Recherche
Pour chaque mode, il y a une barre de recherche qui renvoie une liste des chansons compatibles.
##### Paroles
Enfin pour afficher les paroles on peut cliquer sur les chansons.

## Amélioration
Ajout d'un onglet pour avoir le classement des chansons.
Rajouter des graphiques avec le classement des chansons.
Améliorer graphiquement le site.


*Fait par PHILIPPE Adrien et GUERROIS Théo*
