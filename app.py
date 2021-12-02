import flask

from DAL.DBTemperature import DBTemperature
from DAL.DBHumidity import DBHumidity
from DAL.DBStatus import DBStatus
from DAL.DBAll import DBAll
from DAL.DBUser import DBUser
from dotenv import load_dotenv
import os
from flask import Flask, json, request, make_response, redirect
from flask_cors import CORS, cross_origin
from cryptography.fernet import Fernet

from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime

from Models.User import User

load_dotenv()
frontend_site= os.environ.get("FRONTEND_SITE")

f = Fernet(os.environ.get('REQUEST_SECRET'))

app = Flask(__name__)
CORS(app, resources={r"*": {"origins":["http://localhost:3000","https://localhost:3000"]}})
temperature = DBTemperature()
humidity = DBHumidity()
status = DBStatus()
all_data = DBAll()

users = DBUser()


def redirect_path(path, code = 301, delete_cookie = False):
    response = redirect("{}/{}".format(frontend_site, path), code)
    if delete_cookie:
        response.delete_cookie("auth")
    return response


def decode_token(token):
    try:
        values = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms='HS256')
        return values
    except jwt.ExpiredSignatureError:
        return None

    except Exception as e:
        print(e)

@app.route('/register', methods=['post'])
def register_user():
    data = request.get_json()
    print(data)
    if data is None:
        return app.response_class(
            response={"registration empty"},
            status=401,
            mimetype='application/json'
        )
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    exists = users.insert_user(new_user.public_id,new_user.name, new_user.password, new_user.admin)
    if exists is False:
        return app.response_class(
            response={"user already exists"},
            status=401,
            mimetype='application/json'
        )
    return app.response_class(
            response={"registered successfully"},
            status=201,
            mimetype='application/json'
        )
@app.route('/logout', methods=['post'])
def logout_user():
    if request.cookies.get("auth"):
        response = redirect_path("login", delete_cookie=True)
        return response
    return make_response("Already logged out", 400)

@app.route('/login', methods=['post'])
def login_user():
    if request.cookies.get("auth"):
        values = decode_token(request.cookies.get("auth"))
        if values is None:
            redirect_path("login", 302, True)
        if values['admin'] is True:
            response = redirect_path("")
        return response
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return app.response_class(
            response={"login required"},
            status=401,
            mimetype='application/json'
        )
    user = users.select_user(auth.username)
    # print(user)
    if user is None:
        return app.response_class(
            response={"user doesn't exist"},
            status=401,
            mimetype='application/json',
        )
    # print(user['password'])
    if check_password_hash(user['password'], auth.password):
        token = jwt.encode({'public_id':user['uuid'], 'admin': user['admin'], 'exp':datetime.datetime.utcnow()+datetime.timedelta(
            seconds=10
            # minutes=30
        )},
                           os.environ.get("JWT_SECRET"), algorithm='HS256')
        # print(token)
        response = redirect_path("", 302)
        response.set_cookie("auth", value=str(token), httponly=True, max_age=60*60*24*365*1)
        return response

    return app.response_class(
            response={"wrong credentials"},
            status=401,
            mimetype='application/json',
        )

@app.route('/')
def get_all_temp_data():  # put application's code here
    token = request.cookies.get("auth")
    if token is None:
        response = redirect_path("login", 302)
        return response
    print(token)
    values = decode_token(token)
    if values is None:
        return redirect_path("login", 302, True)
    if values['admin'] is False:
        response = redirect_path("login", 302, True)
        return response
    print(values)
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
    string = ""
    for i in content.keys():
        string += str(content[i])
    print(string);
    if f.decrypt(bytes(header_security,'ascii')) != bytes(string,'ascii'):
        return app.response_class(status=401)
    if not("temperature" in content and "humidity" in content and "status" in content):
        return app.response_class(response="Post request needs to contain humidity, temperature and status in order to work.", status=400)
    result_temp = temperature.insert_all_temperatures(content["temperature"])
    result_humidity = humidity.insert_all_humidities(content["humidity"])
    result_status = status.insert_all_status(content["status"])
    return_val = {"temperature":result_temp, "humidity": result_humidity, "status":result_status}
    return app.response_class(response=json.dumps(return_val), status=201, mimetype='application/json')

@app.route('/api/check', methods = ['GET'])
def check():
    return make_response("Server online", 200)

if __name__ == '__main__':
    app.run()
