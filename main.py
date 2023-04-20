import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
from datetime import datetime, time
import logging


class MyClient(discord.Client):

    def __init__(self, intents, cousinade_channel):
        self._cousinade_channel = cousinade_channel
        super().__init__(intents=intents)


    async def on_ready(self):
        logging.info("Logged in as")
        logging.info(self.user)
        logging.info("------")

        help_title = "Voici la liste de mes fonctionnalités :"
        help_contents = [
            "!help : Affiche l'aide",
            "!quand : Affiche la date de la cousinade",
            "!nouvelle_date : Défini une nouvelle date pour la cousinade (Pas implémenté)",
            "!start : Lance le compte à rebours (Pas implémenté)",
            "!stop : Arrête le compte à rebours (Pas implémenté)",
        ]
        self._help_message = self._generate_help_message(help_title, help_contents)

        self._jour_cousinade = datetime(2023, 5, 27)


        # self.printer.start()
        await self.jour_avant_la_cousinade.start()

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == self.user:
            return

        match (message.content):
            case "!help":
                await message.channel.send(self._help_message)
            case "!quand":
                await message.channel.send(
                    f"La cousinade aura lieu le **{self._jour_cousinade.day}/{self._jour_cousinade.month}/{self._jour_cousinade.year}**"
                )

    # 12h = 10 en utc
    @tasks.loop(time=time(hour=12), reconnect=True)
    async def jour_avant_la_cousinade(self):
        logging.info("JOUR AVANT LA COUSINADE")
        jour_restants = (self._jour_cousinade - datetime.now()).days
        pluriel = "s"

        logging.info(f"Il reste {jour_restants} jours")
        if jour_restants < 0:
            return

        if jour_restants == 1:
            pluriel = ""

        channel = self.get_channel(self._cousinade_channel)
        await channel.send(
            f"Vu que Eva ne fait plus son travail, je suis obligé de m'y mettre ...\nPlus que **{jour_restants} jour{pluriel}** avant la cousinade"
        )

    def _generate_help_message(self, help_title, help_contents):
        sizes = [len(msg) for msg in help_contents]
        sizes.append(len(help_title))
        max_size = max(sizes)

        help_message = '```\n+' + '-'*(max_size+2) + '+' + '\n' + \
            '| ' + help_title + ' '*((max_size+1) - len(help_title)) + '|\n' + \
            '+' + '-'*(max_size+2) + '+' + '\n'
        for msg in help_contents:
            help_message += '| ' + msg + ' '*((max_size+1) - len(msg)) + '|\n'
        help_message += '+' + '-'*(max_size+2) + '+```'

        return help_message
    
    # @tasks.loop(seconds=5.0)
    # async def printer(self):
    #     logging.info("COUCOU")


def main():
    logging.basicConfig(encoding="utf-8", level=logging.INFO)
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    COUSINADE_CHANNEL = os.getenv("COUSINADE_CHANNEL")

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents, cousinade_channel=COUSINADE_CHANNEL)
    client.run(TOKEN)

if __name__ == "__main__":
    main()