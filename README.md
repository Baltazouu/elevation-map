# elevation-map

# Guide d'installation

Ce projet utilise un environnement virtuel Python (venv) pour la gestion des dépendances. Suivez les étapes ci-dessous pour configurer votre environnement et installer les dépendances nécessaires.

## Prérequis

- **Python** (version 3.x recommandée)
- **pip** (gestionnaire de paquets Python)

## Création d'un environnement virtuel

1. Ouvrez un terminal ou une invite de commande.
2. Exécutez la commande suivante pour créer un environnement virtuel nommé `venv` :
   ```sh
   cd elevation-map
   python -m venv venv
   ```
3. Activez l'environnement virtuel :
    - **Windows** :
      ```sh
      venv\Scripts\activate
      ```
    - **Mac/Linux** :
      ```sh
      source venv/bin/activate
      ```

## Installation des dépendances

1. Assurez-vous que l'environnement virtuel est activé.
2. Installez les dépendances depuis le fichier `requirements.txt` :
   ```sh
   pip install -r requirements.txt
   ```

## Génération du fichier `requirements.txt`

Si vous devez créer un fichier `requirements.txt` contenant toutes les dépendances nécessaires, utilisez la commande suivante :
```sh
pip freeze > requirements.txt
```

## Dépendances utilisées

Ce projet utilise les bibliothèques suivantes :
- `gpxpy` : Manipulation des fichiers GPX
- `numpy` : Calculs scientifiques et manipulation de tableaux
- `folium` : Visualisation de cartes interactives
- `matplotlib` : Création de graphiques
- `geopy` : Calcul de distances géographiques
- `functools` : Optimisation avec `lru_cache`
- `os`, `sys` : Modules standards pour la gestion des fichiers et des chemins

## Désactivation de l'environnement virtuel

Lorsque vous avez terminé, vous pouvez désactiver l'environnement virtuel avec :
```sh
deactivate
```

## Exécution du projet

Une fois les dépendances installées, vous pouvez exécuter votre script en activant l'environnement virtuel et en lançant :
```sh
python script.py
```


## Lancer l'API
`uvicorn scripts.map_api:app --reload`

## Côté front

```
cd elevation-app
npm i
```
