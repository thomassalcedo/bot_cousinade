import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv
from datetime import datetime, time
import logging


logging.basicConfig(encoding="utf-8", level=logging.INFO)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
COUSINADE_CHANNEL = os.getenv("COUSINADE_CHANNEL")
# TEST_CHANNEL = os.getenv("TEST_CHANNEL")
jour_cousinade = datetime(2023, 5, 27)

intents = discord.Intents.default()
intents.message_content = True
help_command = commands.DefaultHelpCommand(no_category="Commandes")

bot = commands.Bot(command_prefix="!", help_command=help_command, intents=intents)


@bot.event
async def on_ready():
    logging.info("Logged in as")
    logging.info(bot.user)
    logging.info("------")

    # printer.start()
    jour_avant_la_cousinade.start()


@bot.event
async def on_message(message):
    """Appelée quand un message est reçu."""
    if message.author == bot.user:
        return

    await bot.process_commands(message)


@bot.command()
async def quand(ctx):
    """Affiche la date de la cousinade"""
    await ctx.send(
        f"La cousinade aura lieu le **{jour_cousinade.day}/{jour_cousinade.month}/{jour_cousinade.year}**"
    )


@bot.command()
async def start(ctx):
    """Lance le compte à rebours (Pas implémenté)"""
    pass


@bot.command()
async def stop(ctx):
    """Arrête le compte à rebours (Pas implémenté)"""
    pass


async def nouvelle_date(ctx):
    """Défini une nouvelle date pour la cousinade (Pas implémenté)"""
    pass


# 8h = 10h en utc askip
@tasks.loop(time=time(hour=8), reconnect=True)
async def jour_avant_la_cousinade():
    logging.info("JOUR AVANT LA COUSINADE")
    jour_restants = (jour_cousinade - datetime.now()).days
    pluriel = "s"

    logging.info(f"Il reste {jour_restants} jours")
    if jour_restants < 0:
        return

    if jour_restants == 1:
        pluriel = ""

    channel = bot.get_channel(int(COUSINADE_CHANNEL))
    await channel.send(
        f"Vu que Eva ne fait plus son travail, je suis obligé de m'y mettre ...\nPlus que **{jour_restants} jour{pluriel}** avant la cousinade"
    )


# @tasks.loop(seconds=5.0)
# async def printer():
#     logging.info("COUCOU")

bot.run(TOKEN)
