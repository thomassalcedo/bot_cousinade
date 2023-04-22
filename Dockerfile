FROM python:3.10.6

# Ajout des fichiers dans le conteneur
ADD --chown=root:root cousinade.service /etc/systemd/system/cousinade.service
ADD --chown=root:root .env /opt/bot_cousinade/.env

# Création de l'utilisateur cousinade
RUN useradd --system --no-create-home --shell=/sbin/nologin cousinade
RUN chown -R root:cousinade /opt/bot_cousinade
RUN chmod -R 775 /opt/bot_cousinade

# Création de l'environnement virtuel et installation des librairies
RUN python3 -m venv /opt/bot_cousinade \
&& /opt/bot_cousinade/bin/pip3 install -r requirements.txt

# Redémarrage des daemons et démarrage du service cousinade
RUN systemctl daemon-reload \
&& systemctl enable cousinade.service \
&& systemctl start cousinade.service

CMD tail -f /dev/null 

# Pour le build :
# docker build -t bot_cousinade .

# Pour lancer le conteneur :
# docker run -d bot_cousinade