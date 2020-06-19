# bot.py
import os
import requests
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AIRTABLE_AUTH = os.getenv('AIRTABLE_AUTH')

client = discord.Client()

def get_overheard():
    """
    Returns a quote from the Overheard Airtable.
    """
    headers = {'Authorization': f'Bearer {AIRTABLE_AUTH}'}
    params = (('maxRecords', '50'),('view', 'Grid view'))
    response = requests.get('https://api.airtable.com/v0/appK9gYuFThtDMzPz/Quotes', headers=headers, params=params)
    choices = [r.get('fields').get('Quote') for r in response.json().get('records') if r.get('fields') != None]
    return random.choice(choices)

def lookup_referrals(company_code):
    """
    Looks up who we know in our Referral Network Airtable (given a company).
    """
    import requests
    headers = {'Authorization': f'Bearer {AIRTABLE_AUTH}'}
    params = (('maxRecords', '50'),('view', 'API'))
    response = requests.get('https://api.airtable.com/v0/appvE25wUsaju5CjV/Network', headers=headers, params=params)
    choices = {r.get('fields').get('Name'): r.get('fields').get('CompanyCode') for r in response.json().get('records') if r.get('fields') != None}
    
    people = []
    company = ''
    for k, v in choices.items():
        if v.lower() == company_code.lower():
            company = v
            people.append(k)
    
    if len(people) > 0:
        content = f"Here's who we might know at {company_code}: {', '.join(people)}. View more at http://go.mdb.dev/referrals"
        return content
    else:
        raise Exception("We don't know anyone.")

@client.event
async def on_ready():
    """
    Prints a debug message when the bot connects.
    """
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    """
    This is triggered every time a message is sent.
    TODO: Move this to Bot architecture instead of Client architecture!
    """
    if message.author == client.user:
        return

    if 'lunch' in message.content:
        response = '@aarushi @shaurya @shomil @vaibhav @kanyes @sumukh-shivakumar @victor-sun when\'s lunch?'
        await message.channel.send(response)

    if message.content.startswith('/job'):
        try:
            workplace = message.content.split(' ')[1]
            await message.channel.send(lookup_referrals(workplace))
        except Exception as e:
            print(e)
            company = ' '.join(message.content.split(' ')[1:])
            await message.channel.send(f'Uh oh! I couldn\'t find anyone at {company}. View the network: http://go.mdb.dev/referrals')

    if message.content == '/overheard':
        response = get_overheard()
        await message.channel.send(response)

client.run(TOKEN)
