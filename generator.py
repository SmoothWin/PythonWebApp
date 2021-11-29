#this is a test file done in order to extract simulate what we need to do overall
#ps this also shows the encrypted version of the f.encrypt(bytes(str(list(dicti.values())), 'ASCII'))
#where we can get the encrypted body values to put into the security-check header
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

dicti = {
  "temperature": [
    {
      "date_time": "2021-11-17 22:21:36",
      "temperature": 26.0
    }
  ],
  "humidity": [
    {
      "date_time": "2021-11-17 22:21:36",
      "humidity": 0.42
    }
  ],
  "status": [
    {
      "date_time": "2021-11-17 22:21:36",
      "online": 1
    }
  ]
}


load_dotenv()
print(Fernet.generate_key())
f = Fernet(os.environ.get('REQUEST_SECRET'))
key = Fernet.generate_key()
print(list(dicti.values()))
string = ""
print(dicti.items())
for i in dicti.keys():
  string += str(dicti[i])
print(string);
token = f.encrypt(bytes(str(list(dicti.values())), 'ASCII'))
print("Token: {}".format(token))
print(f.decrypt(bytes('gAAAAABhldLPYQshYou9l7c-rjGIc2aG8-zv9I5P-GgCCDxh6Q-paYleJC4Bf89QdWpa2R7s9val9v4CA0fpVTyRd_XwCcP9CsSz4SJRyYFOZ9w1-nGG0yUznYvMNeaad0b3037PVQRljW1Hg8XhDQdd1Gy74Qv4jc5kPl7ww17L8vm-wHEBgy0G7GSUP-Um0uZm-E1MaSvVovCynzLz4qW0oubxsCMg5xefZ12kqcoBDdQ488cetWL6i6OD-MVMUwxco8pIc778OOvVcuGYi8yOBXg4iOdeMe2rbCi9D7z2zQNaMjk6q0k=','ascii')))


