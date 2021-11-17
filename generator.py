#this is a test file done in order to extract simulate what we need to do overall
#ps this also shows the encrypted version of the f.encrypt(bytes(str(list(dicti.values())), 'ASCII'))
#where we can get the encrypted body values to put into the security-check header
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

dicti = {'temperature': [{'date_time': 'Sat, 13 Nov 2021 19:38:29 GMT', 'temperature': 12}], 'humidity': [{'date_time': 'Sat, 13 Nov 2021 19:38:29 GMT', 'humidity': 0.23}], 'status': [{'date_time': 'Sat, 13 Nov 2021 19:38:29 GMT', 'online': True}]}

load_dotenv()
f = Fernet(os.environ.get('REQUEST_SECRET'))
key = Fernet.generate_key()
print(list(dicti.values()))
token = f.encrypt(bytes(str(list(dicti.values())), 'ASCII'))
print("Token: {}".format(token))


