# Compétence 5 : Développer une API mettant à disposition le jeu de données
## Environnement d'execution
<b> Python </b>: 3.10.13 <br>
Pour installer les dépendances, selon l'OS utilisé :
  - <b>requirements_w.txt</b> : pour windows (Windows 10)
  - <b>requirements.txt</b> : autres ( foncitonnel sous Ubuntu 20.0.4 )

## Commandes utiles
Faire tourner les tests : 
```
python -m pytest tests/
```
Lancement de l'application en local : 
```
cd app
uvicorn main:app --reload
```
