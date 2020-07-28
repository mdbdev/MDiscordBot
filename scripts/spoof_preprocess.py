import glob, json, os
from collections import defaultdict
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()
CRYPTO_KEY = os.getenv('CRYPTO_KEY')

path = '/Users/shomil/Documents/Datasets/personal/facebook/messages/inbox/'

folders = ['mdbsp19OLD_DTfVjN88rA/', 'mdbf18_ZrUYaQmPJw/', 'MDBducksofa_SY4Xa7bzyg/', '1MDB_AVGyzYtyjw/', 'FALL2019DEPRECATEDMDBLship_Evy4VoLVXw/', 'MDBExecNotTables_FAXF8id-LA/', 'MDBLeadershipWearemostlyIndiansDear_cOKAwhqKhQ/']

messages = defaultdict(list)
for folder in folders:
    file = path + folder + 'message_1.json'
    data = json.load(open(file))
    for message in data.get('messages'):
        if message.get('content') != None and 'nickname' in message['content']:
            message = message.get('content')
            if 'set the nickname for' not in message: continue
            message = message.split(' set the nickname for ')[1]
            message = message.split(' to ')
            name = message[0]
            content = ' '.join(message[1:])
            messages[name].append(content)

print(messages)

json_str = json.dumps(messages)
cipher_suite = Fernet(CRYPTO_KEY)
encoded_text = cipher_suite.encrypt(json_str.encode())
with open('encoded_nicknames.txt', 'wb') as file:
    file.write(encoded_text)

# Test Decryption
with open('encoded_nicknames.txt', 'rb') as file:
    encoded_text = file.read()
    cipher_suite = Fernet(CRYPTO_KEY)
    decoded_json = cipher_suite.decrypt(encoded_text).decode('utf8')
    print(json.loads(decoded_json).keys())