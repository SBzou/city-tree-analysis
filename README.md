# Analyse des arbres de Grenoble

## Mots clés

- Extractions de connaissance
- Data Mining
- Machine Learning
- Prédictions
- Statistiques

## Objectif

Ce dépôt Git répond au défi proposé lors de l'EGC 2017, conférence sur l'extraction et la gestion de connaissance : http://egc2017.imag.fr/defi/index.html

A partir d'un jeu de données sur les arbres de la ville de Grenoble, le défi consiste à : 
- **Machine Learning** : tâche de prédiction visant à déterminer, à partir des données disponibles, si l’arbre a ou non un défaut et dans l’affirmative lequel, sachant qu’un arbre peut présenter plusieurs défauts.
- **Extraction de Connaissances** : la seconde tâche, plus ouverte, vise à appliquer des techniques d’extraction et de gestion de connaissances afin de mieux connaitre l’état du « parc végétal » de Grenoble, de mieux comprendre son évolution et de fournir des préconisations pour faciliter son entretien. 

## Arborescence 
- **data** : contient toutes les données
- **map** : contient les maps construites via le fichier python map
-  **stats** : contient toutes les statistiques construites via le fichier python stats
- `data_exploration.py` : premier fichier à exécuter pour traiter les données initiales. Ce fichier génère les données traitées **donnees-traitees.csv**
- `model.py` : contient tout les modèles du dépôt Git visant à prédire l'état des arbres de Grenoble
- `school_and_park.py` : à partir de données sur les écoles et les parcs de Grenoble extraites personnellement, apporte des informations supplémentaires sur les arbres.

## Installation

Après avoir copié le dépôt Git et s'être placé dans le répertoire, on peut commencer par exécuter le fichier **data_exploration.py**
```
python data_exploration.py
```
Le fichier **donnees-traitees.csv** est généré. On peut exécuter le fichier  : 

On peut exécuter les fichiers map, model, school_and_park et stats dans l'ordre souhaité : 
```
python map.py
python model.py
python school_and_park.py
python stats.py
```


# Travail accompli

## Traitement des données

Initialement, le dépôt Git ne contient que le fichier **donnees-defi-egc.csv**. On propose un premier fichier `data_exploration.py` traitant ces données. Parmis les nombreuses opérations réalisées, on peut citer : 
- l'étude des données, via des comparaisons, des similarités cosinus ou des corrélations 
- la suppression des colonnes inutiles
- le retrait des valeurs manquantes
- la numérisation de certains champs pour améliorer les résultats des modèles d'IA.
- la conversion des coordonnées
- l'ajout des champs associé à de nouvelles classes détecté durant l'étude des données
- le changement de nom de colonnes jugées mal nommées

On génère le fichier **donnees-traitees.csv** qui sera utilisé par les autres fichiers python.

## Machine Learning

Une fois les données traitées, on explore plusieurs modèles d'apprentissage automatique pour prédire l'état des arbres de Grenoble. Voici les résultats obtenus avec différents modèles :
- Le modèle **Random Forest** a été entraîné et évalué avec les données prétraitées. Voici l'accuracy obtenue sur l'ensemble de test : 86%.
- Le modèle **Decision Tree**, avec une profondeur maximale de 3, a été entraîné et évalué. Voici l'accuracy obtenue sur l'ensemble de test : 83%.
- Le modèle **Naive Bayes** a été entraîné et évalué. Voici le score obtenu sur l'ensemble de test : 70%.
- Le modèle de régression logistique a été entraîné et évalué. Voici le score obtenu sur l'ensemble de test : 83%.
- Le modèle **K-Nearest Neighbors** a été entraîné et évalué. Voici le score obtenu sur l'ensemble de test : 84%.
- Le modèle Linear Support Vector Machine (**SVM**) a été entraîné et évalué. Voici le score obtenu sur l'ensemble de test : 70%.
- Le modèle **Bagging** avec 10 arbres de décision a été entraîné et évalué. Voici le score obtenu sur l'ensemble de test : 86%.
- Le réseau neuronal séquentiel a été construit et entraîné avec 10 epochs. Voici le score obtenu sur l'ensemble de test : 68%.

Ces résultats offrent une vue d'ensemble des performances des différents modèles sur la tâche de prédiction de l'état des arbres de Grenoble. Les deux modèles ayant eu les meilleures performances sont le modèle **Random Forest** et le modèle **Bagging** avec un score de 86%.

## Etude cartographique

Le fichier `map.py` génère des cartes interactives en format HTML pour visualiser la distribution spatiale des arbres de Grenoble en fonction de différentes caractéristiques. On peut également comparer ces cartes avec d'autres cartes disponible en ligne, par exemple la répartition du prix du mètre carré ou la proximité avec des fleuves. Voici une description de chaque fonction du fichier :
- show_default_map : affiche une carte avec des marqueurs rouges pour les arbres présentant un défaut et des marqueurs verts pour les arbres sans défaut.
- show_one_kind_default_map : affiche une carte avec des marqueurs rouges pour les arbres ayant un type spécifique de défaut et des marqueurs verts pour les arbres sans ce défaut.
- show_number_default_map : affiche une carte où chaque marqueur représente le nombre total de défauts pour un arbre. Les couleurs varient de vert (pas de défaut) à noir (quatre défauts).
- show_year_default_map : affiche une carte avec des marqueurs verts pour les arbres plantés avant l'année spécifiée par l'utilisateur.

Toutes les maps sont présentes dans le dossier **map**.

## Analyses complémentaires

### Etude de la proximité avec une école ou un parc

On se pose la question suivante, l'état de l'arbre est-il influencer par sa proximité avec une école ou un parc ? On génère donc deux fichier csv nommés **positions_ecoles.csv** et **positions_parcs** indiquant pour chaque écoles et parc de Grenoble son nom et ses coordonnées.

Le fichier `school_and_park.py` analyse la relation entre la proximité des arbres avec des écoles et des parcs. 

En ayant choisi un seuil de 300m délimitant si un arbre est prés d'une école ou non, voici les résultats obtenues : 
- Proximité avec une école : 67% des arbres n'ont pas de défaut
- Dans un parc : 69% des arbres n'ont pas de défaut

### Statistiques

Le fichier `stats.py` génère diverses statistiques à partir du jeu de données sur les arbres. Voici une description des principales fonctions :
- `get_all_values_repartition()` : crée des fichiers dans le dossier `stat/value_count/` pour chaque colonne du dataframe. Chaque fichier contient la répartition des différentes valeurs pour la colonne correspondante.
- `get_columns_cosinus_similarities(col1, col2)` : calcule la similarité cosinus entre deux colonnes numériques `col1` et `col2` du dataframe.
- `get_columns_cosinus_similarities_stade_developpement()` : calcule la similarité cosinus entre les colonnes 'STADEDEDEVELOPPEMENT' et 'STADEDEVELOPPEMENTDIAG' après avoir numérisé ces colonnes.
- `get_matrix_similarities()` : construit un fichier `stat/similarities/defaut.txt` contenant toutes les combinaisons de similarités pour les colonnes : 'DEFAUT', 'Collet', 'Houppier', 'Racine', 'Tronc'.
- `get_defaut_proportion_for_stade_developpement_difference()` : analyse les différences entre les colonnes 'STADEDEDEVELOPPEMENT' et 'STADEDEVELOPPEMENTDIAG' pour évaluer les proportions de défauts pour chaque colonne. Les résultats sont enregistrés dans le fichier `stat/percentages/stadeDeveloppementDifferences.txt`.
- `get_defaut_proportion_for_year()` : analyse les proportions de défauts pour chaque année entre 2004 et 2015. Les résultats sont enregistrés dans des fichiers spécifiques pour chaque année.
- `get_defaut_proportionF_for_adr_secteur()` : analyse les proportions de défauts pour chaque valeur unique de 'ADR_SECTEUR'. Les résultats sont enregistrés dans des fichiers spécifiques pour chaque valeur.
-  `value_count(dataFrame, colName, value, lenght)` : retourne le pourcentage d'occurrences de `value` dans la colonne `colName` du dataframe `dataFrame`.
- `get_defaut_proportion_for_traitement_chenilles()` : analyse les proportions de défauts pour chaque valeur unique de 'TRAITEMENTCHENILLES'. Les résultats ne montrent pas de différences significatives entre les différentes priorités.
- `get_defaut_proportion_for_trottoir()` : analyse les proportions de défauts pour chaque valeur unique de 'TROTTOIR'. Les résultats montrent des différences, mais elles ne sont pas considérées comme pertinentes.
- `get_defaut_proportion_for_type_implantation_plu()` : analyse les proportions de défauts pour chaque valeur unique de 'TYPEIMPLANTATIONPLU'. Les résultats ne montrent pas de différences significatives.

Tout les résultats de ces statistiques sont présents dans le dossiers **stats**
