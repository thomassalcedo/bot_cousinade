import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv, set_key
from datetime import datetime, time
import logging

logging.basicConfig(encoding="utf-8", level=logging.INFO)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
COUSINADE_CHANNEL = os.getenv("COUSINADE_CHANNEL")
# TEST_CHANNEL = os.getenv("TEST_CHANNEL")
DATE = datetime.strptime(os.getenv("DATE"), "%d/%m/%Y")
SENDING = os.getenv("SENDING")

intents = discord.Intents.default()
intents.message_content = True
help_command = commands.DefaultHelpCommand(no_category="Commandes")

bot = commands.Bot(command_prefix="!", help_command=help_command, intents=intents)


@bot.event
async def on_ready():
    logging.info("Logged in as")
    logging.info(bot.user)
    logging.info("------")

    logging.info(f"TOKEN: {TOKEN}")
    logging.info(f"COUSINADE_CHANNEL: {COUSINADE_CHANNEL}")
    logging.info(f"DATE: {DATE}")
    logging.info(f"SENDING: {SENDING}")
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
    await ctx.send(f"La cousinade aura lieu le **{DATE.day}/{DATE.month}/{DATE.year}**")


@bot.command()
async def start(ctx):
    """Lance le compte à rebours"""
    global SENDING
    # os.environ["SENDING"] = "True"
    # SENDING = os.environ["SENDING"]
    SENDING = "True"
    # set_key(".env", "SENDING", os.environ["SENDING"])
    set_key(".env", "SENDING", SENDING)
    logging.info("Setting the SENDING parameter to True")
    await ctx.send("Le compte à rebours sera envoyé tous les jours à 10h")


@bot.command()
async def stop(ctx):
    """Arrête le compte à rebours"""
    global SENDING
    # os.environ["SENDING"] = "False"
    # SENDING = os.environ["SENDING"]
    SENDING = "False"
    set_key(".env", "SENDING", SENDING)
    logging.info("Setting the SENDING parameter to False")
    await ctx.send("Le compte à rebours ne sera plus effectué")


@bot.command()
async def nouvelle_date(
    ctx,
    date: str = commands.parameter(
        default=None, description='Une date au format "jj/mm/aaaa"'
    ),
):
    """Défini une nouvelle date pour la cousinade"""
    global DATE
    if date is None:
        await ctx.send('Une date au format "jj/mm/aaaa" doit être fournie.')
    else:
        try:
            DATE = datetime.strptime(date, "%d/%m/%Y")
            # os.environ["DATE"] = f"{DATE.day}/{DATE.month}/{DATE.year}"
            set_key(".env", "DATE", f"{DATE.day}/{DATE.month}/{DATE.year}")
            logging.info(f"Setting the DATE parameter to {DATE}")
            await ctx.send(
                f"Nouvelle date définie au **{DATE.day}/{DATE.month}/{DATE.year}**"
            )
        except:
            await ctx.send(
                f'Mauvais entrée pour **{date}**. Une date au format "jj/mm/aaaa" doit être fournie.'
            )


# 8h = 10h en utc askip
@tasks.loop(time=time(hour=8), reconnect=True)
async def jour_avant_la_cousinade():
    if SENDING == "True":
        logging.info("JOUR AVANT LA COUSINADE")
        jour_restants = (DATE - datetime.now()).days +1
        pluriel = "s" if jour_restants > 1 else ""

        logging.info(f"Il reste {jour_restants} jours")
        
        if jour_restants >= 0:
            channel = bot.get_channel(int(COUSINADE_CHANNEL))
            if jour_restants == 0:
                await channel.send(
                    f"C'est la cousinade !!!"
                )
            else:
                await channel.send(
                    f"Plus que **{jour_restants} jour{pluriel}** avant la cousinade"
                )
    else:
        logging.info("Pas d'envoi")


# @tasks.loop(seconds=5.0)
# async def printer():
#     if SENDING == "True":
#         logging.info("COUCOU")
#     else:
#         pass


bot.run(TOKEN)
