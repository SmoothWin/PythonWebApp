from DAL.DBTemperature import DBTemperature
from DAL.DBHumidity import DBHumidity
from DAL.DBStatus import DBStatus
from DAL.DBAll import DBAll
from dotenv import load_dotenv
import os
from flask import Flask, json, request
from cryptography.fernet import Fernet


load_dotenv()
f = Fernet(os.environ.get('REQUEST_SECRET'))

app = Flask(__name__)
temperature = DBTemperature()
humidity = DBHumidity()
status = DBStatus()
all_data = DBAll()

@app.route('/')
def hello_world():  # put application's code here
    all_temp = temperature.select_all_temperatures()
    all_hum = humidity.select_all_humidities()
    all_stat = status.select_all_status()
    print(all_temp)
    print(all_hum)
    print(all_stat)

    response = app.response_class(
        response=json.dumps({"temperatures":all_temp, "humidities":all_hum, "status":all_stat}),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/send', methods = ['POST'])
def send_data():
    header_security = request.headers['security-check']
    content = request.json

    if f.decrypt(bytes(header_security,'ascii')) != bytes(str(list(content.values())),'ascii'):
        return app.response_class(status=401)
    print(content)
    if not("temperature" in content and "humidity" in content and "status" in content):
        return app.response_class(response="Post request needs to contain humidity, temperature and status in order to work.", status=400)
    result_temp = temperature.insert_all_temperatures(content["temperature"])
    result_humidity = humidity.insert_all_humidities(content["humidity"])
    result_status = status.insert_all_status(content["status"])
    return_val = {"temperature":result_temp, "humidity": result_humidity, "status":result_status}
    return app.response_class(response=json.dumps(return_val), status=201, mimetype='application/json')

def str_to_binary(s):
    bin_conv = []
    for c in s:
        ascii_val = ord(c)

        binary_val = bin(ascii_val)
        bin_conv.append(binary_val[2:])
    return (' '.join())
if __name__ == '__main__':
    app.run()
