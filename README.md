# bot_cousinade
Un bot discord pour connaitre le nombre de jour avant la cousinade.

## Prerequis
### Installer les librairies python
Il est recommandé de la faire dans un venv python (`python3 -m venv`).  

Installation avec **pip** : `pip3 install -r requirements.txt`  

### Créer le fichier d'environnement
Il faut aussi créer un fichier **.env** à la racine du projet contenant les variables suivante :  
```
DISCORD_TOKEN={Le token de votre bot}
COUSINADE_CHANNEL={L'ID du channel}
DATE={La date de la cousinade}
SENDING={'True' ou 'False' selon si vous voulez les notifications du compte à rebours ou non}
```

## Pour le lancer avec Docker :
Il faut créer le fichier .env comme précédemment.  
**Attention** : Ce fichier n'est **pas persistant**, si le conteneur redémarre le fichier sera **restauré**.  
(TODO: rendre le fichier d'env persistant)

Pour construire le conteneur :  
`docker build -t bot_cousinade .`

Pour lancer le conteneur :  
`docker run -d bot_cousinade`
