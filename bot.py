# bot.py
import os

import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AIRTABLE_AUTH = os.getenv('AIRTABLE_AUTH')

client = discord.Client()

def get_overheard():
    import requests
    headers = {
        'Authorization': f'Bearer {AIRTABLE_AUTH}',
    }
    params = (
        ('maxRecords', '50'),
        ('view', 'Grid view'),
    )
    response = requests.get('https://api.airtable.com/v0/appK9gYuFThtDMzPz/Quotes', headers=headers, params=params)
    choices = [r.get('fields').get('Quote') for r in response.json().get('records') if r.get('fields') != None]
    return random.choice(choices)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'lunch' in message.content:
        response = '@aarushi when\'s lunch?'
        await message.channel.send(response)

    if message.content == '/overheard':
        response = get_overheard()
        await message.channel.send(response)

client.run(TOKEN)
