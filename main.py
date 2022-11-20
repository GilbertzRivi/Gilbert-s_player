from discord.enums import ActivityType
from client import client
from discord import Activity
import os
from dotenv import load_dotenv
from music import *

load_dotenv('.env')

@client.event
async def on_ready():
    print(f'logged in as {client.user.name}')
    await client.change_presence(activity=Activity(name='.help', type=ActivityType.watching))
    client.voice = None
    for file in os.listdir('music'):
        os.remove("music/"+file)
    
client.run(os.getenv('TOKEN'))