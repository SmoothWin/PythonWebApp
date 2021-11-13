from DAL.DBTemperature import DBTemperature
from flask import Flask, jsonify

app = Flask(__name__)
temperature = DBTemperature()

@app.route('/')
def hello_world():  # put application's code here
    all_temp = temperature.select_all_temperatures()
    print(all_temp)
    return jsonify(all_temp)


if __name__ == '__main__':
    app.run()
