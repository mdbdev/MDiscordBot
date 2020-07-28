import json
from cryptography.fernet import Fernet
import random

def whois(person, crypto_key):
    with open('scripts/encoded_nicknames.txt', 'rb') as file:
        encoded_text = file.read()
        cipher_suite = Fernet(crypto_key)
        decoded_json = cipher_suite.decrypt(encoded_text).decode('utf8')
        nicknames = json.loads(decoded_json)
        
    chosen_person = ''
    content = []
    for k, v in nicknames.items():
        if person.lower() in k.lower():
            content = v
            chosen_person = k
    
    if chosen_person == '':
        raise Exception("No person.")

    return random.choice(nicknames[chosen_person])