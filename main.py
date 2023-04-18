import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv
from datetime import datetime, time


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

jour_cousinade = datetime(2023, 5, 27)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user)
    print('------')


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    match (message.content):
        case "!help":
            await message.channel.send("Je ne fais rien de plus pour l'instant")


@discord.ext.tasks.loop(time=time(hour=10), count=None, reconnect=True)
# @discord.ext.tasks.loop(time=time(hour=10, tzinfo=tzinfo.tzname("Europe/Paris")), count=None, reconnect=True)
async def jour_avant_la_cousinade():
    jour_restants = (jour_cousinade - datetime.now()).days
    pluriel = "s"
    
    if (jour_restants < 0):
        return
    
    if (jour_restants == 1):
        pluriel = ""  

    channel = client.get_channel(COUSINADE_CHANNEL)
    await channel.send(f"Vu que Eva ne fait plus son travail, je suis obligé de m'y mettre ...\nPlus que {jour_restants} jour{pluriel} avant la cousinade") 



load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
COUSINADE_CHANNEL = os.getenv("COUSINADE_CHANNEL")

client.run(TOKEN)
