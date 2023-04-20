import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
from datetime import datetime, time
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

jour_cousinade = datetime(2023, 5, 27)


@client.event
async def on_ready():
    logging.info("Logged in as")
    logging.info(client.user)
    logging.info("------")
    # await printer.start()
    await jour_avant_la_cousinade.start()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    match (message.content):
        case "!help":
            await message.channel.send(
                "```\n\
+------------------------------------------+\n\
| Voici la liste de mes fonctionnalités :  |\n\
+------------------------------------------+\n\
| !help : Affiche l'aide                   |\n\
| !quand : Affiche la date de la cousinade |\n\
+------------------------------------------+```"
            )
        case "!quand":
            await message.channel.send(
                f"La cousinade aura lieu le **{jour_cousinade.day}/{jour_cousinade.month}/{jour_cousinade.year}**"
            )


# 12h = 10 en utc
@tasks.loop(time=time(hour=12), reconnect=True)
async def jour_avant_la_cousinade():
    logging.info("JOUR AVANT LA COUSINADE")
    jour_restants = (jour_cousinade - datetime.now()).days
    pluriel = "s"

    logging.info(f"Il reste {jour_restants} jours")
    if jour_restants < 0:
        return

    if jour_restants == 1:
        pluriel = ""

    channel = client.get_channel(COUSINADE_CHANNEL)
    await channel.send(
        f"Vu que Eva ne fait plus son travail, je suis obligé de m'y mettre ...\nPlus que **{jour_restants} jour{pluriel}** avant la cousinade"
    )

# @tasks.loop(seconds=5.0)
# async def printer():
#     logging.info("COUCOU")


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
COUSINADE_CHANNEL = os.getenv("COUSINADE_CHANNEL")

client.run(TOKEN)
