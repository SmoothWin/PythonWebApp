from DAL.DBTemperature import DBTemperature
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)
temperature = DBTemperature()

@app.route('/')
def hello_world():  # put application's code here
    all_temp = temperature.select_all_temperatures()
    print(all_temp)
    temperature.insert_all_temperatures([{"date_time":datetime.now(), "temperature":20},{"date_time":datetime.now(), "temperature":20}])
    return jsonify(all_temp)


if __name__ == '__main__':
    app.run(debug=True)
