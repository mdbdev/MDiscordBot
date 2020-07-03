# bot.py
import os
import requests
import random
import discord
from dotenv import load_dotenv
from scripts.spoof import spoof
from scripts.berkeleytime import lookup_class
from cryptography.fernet import Fernet

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AIRTABLE_AUTH = os.getenv('AIRTABLE_AUTH')
CRYPTO_KEY = os.getenv('CRYPTO_KEY')

client = discord.Client()

def get_random_idea():
    """
    Returns a randomly selected idea from ideas.txt
    """
    ideas = open('scripts/ideas.txt', 'r').read().split('\n')
    return random.choice(ideas)

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

    if message.content.startswith('/idea'):
        await message.channel.send(get_random_idea())

    if message.content.startswith('/spoof'):
        print(str(message.author) + ' used the /spoof command: ' + str(message.content))
        try:
            person = ' '.join(message.content.split(' ')[1:])
            if person.lower() == 'katniss':
                await message.channel.send('i love coding but i also love drinking')
            else:
                await message.channel.send(spoof(person, CRYPTO_KEY))
        except Exception as e:
            print(e)
            await message.channel.send(f'Oh no! I couldn\'t find any messages to train myself on for {person}.')

    if message.content.startswith('/habit'):
        habits = ['Be proactive', 'Begin with the end of mind', 'First things first', 'Think win-win', 'Seek first to understand, then to be understood', 'Synergize!', 'Sharpen the saw!']
        await message.channel.send(random.choice(habits))

    if message.content.startswith('/class'):
        print(str(message.author) + ' used the /class command: ' + str(message.content))
        try:
            code = ' '.join(message.content.split(' ')[1:])
            await message.channel.send(lookup_class(code))
        except Exception as e:
            print(e)
            await message.channel.send('Uh oh! I couldn\'t find information for that class. Perhaps check your formatting?')

    if message.content.startswith('/job'):
        print(str(message.author) + ' used the /job command: ' + str(message.content))
        try:
            workplace = message.content.split(' ')[1]
            await message.channel.send(lookup_referrals(workplace))
        except Exception as e:
            print(e)
            company = ' '.join(message.content.split(' ')[1:])
            await message.channel.send(f'Uh oh! I couldn\'t find anyone at {company}. View the network: http://go.mdb.dev/referrals')

    if message.content == '/overheard':
        print(str(message.author) + ' used the /overheard command: ' + str(message.content))
        response = get_overheard()
        await message.channel.send(response)

    if message.content == '/help':
        response = """
Hey there! Here's what I can do.

**/class [CLASS NUMBER]:** looks up a particular class's enrollment info (try /class 161). Works for CS/EE classes.

**/job [COMPANY]:** looks up who works at a particular company in our referral database (try /job google)

**/overheard** - randomly sends a message from the MDB overheard repository

**/idea** - randomly sends a message from the MDB idea repository (these were auto-generated by the one and only Daniel Andrews)

**/spoof [NAME]:** uses a markov-chain text generator to spoof someone based on their messages in the MDB chats

        """
        await message.channel.send(response)

client.run(TOKEN)
