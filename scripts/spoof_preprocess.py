import glob, json, os
from collections import defaultdict
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()
CRYPTO_KEY = os.getenv('CRYPTO_KEY')

path = '/Users/shomil/Documents/Datasets/personal/facebook/messages/inbox/'

folders = ['mdbsp19OLD_DTfVjN88rA/', 'mdbfa20_mloedchmua/', 'mdbf18_ZrUYaQmPJw/', 'mdbwumbodb_sy4xa7bzyg/', '1MDB_AVGyzYtyjw/']

messages = defaultdict(list)
for folder in folders:
    file = path + folder + 'message_1.json'
    data = json.load(open(file))
    for message in data.get('messages'):
        if message.get('content') != None and 'group photo' not in message['content'] and 'poll' not in message['content'] and 'nickname' not in message['content']:
            messages[message.get('sender_name')].append(message.get('content'))
            
json_str = json.dumps(messages)
cipher_suite = Fernet(CRYPTO_KEY)
encoded_text = cipher_suite.encrypt(json_str.encode())
with open('encoded_messages.txt', 'wb') as file:
    file.write(encoded_text)

# Test Decryption
with open('encoded_messages.txt', 'rb') as file:
    encoded_text = file.read()
    cipher_suite = Fernet(CRYPTO_KEY)
    decoded_json = cipher_suite.decrypt(encoded_text).decode('utf8')
    print(json.loads(decoded_json).keys())