import json
import markovify
from cryptography.fernet import Fernet

def spoof(person, crypto_key):
    with open('scripts/encoded_messages.txt', 'rb') as file:
        encoded_text = file.read()
        cipher_suite = Fernet(crypto_key)
        decoded_json = cipher_suite.decrypt(encoded_text).decode('utf8')
        messages = json.loads(decoded_json)
        
    chosen_person = ''
    content = []
    for k, v in messages.items():
        if person.lower() in k.lower():
            content = v
            chosen_person = k
    
    if chosen_person == '':
        raise Exception("No person.")
        
    text_model = markovify.NewlineText('\n'.join(content))
    sentence = text_model.make_sentence(min_words=1, tries=1000)
    
    return sentence