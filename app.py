from DAL.DBTemperature import DBTemperature
from datetime import datetime
from flask import Flask, jsonify, json, request

app = Flask(__name__)
temperature = DBTemperature()

@app.route('/')
def hello_world():  # put application's code here
    all_temp = temperature.select_all_temperatures()
    print(all_temp)
    # temperature.insert_all_temperatures([])
    response = app.response_class(
        response=json.dumps(all_temp),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/send', methods = ['POST'])
def send_data():
    content = request.json
    result = temperature.insert_all_temperatures(content["temperature"])
    print(result)
    return app.response_class(response=result, status=201, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
