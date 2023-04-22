# bot_cousinade
Un bot discord pour connaitre le nombre de jour avant la cousinade.

## Prerequis
### Installer les librairies python
Il est recommandé de la faire dans un venv python (`python3 -m venv`).  

Installation avec **pip** : `pip3 install -r requirements.txt`  

Il faut aussi créer un fichier **.env** à la racine du projet contenant les variables suivante :  
```
DISCORD_TOKEN={Le token de votre bot}
COUSINADE_CHANNEL={L'ID du channel}
```

## Pour le lancer avec Docker :
Il faut créer le fichier .env comme précédemment.  

Pour construire le conteneur :  
`docker build -t bot_cousinade .`

Pour lancer le conteneur :  
`docker run -d bot_cousinade`
