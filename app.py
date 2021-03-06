from DAL.DBTemperature import DBTemperature
from DAL.DBHumidity import DBHumidity
from DAL.DBStatus import DBStatus
from DAL.DBUser import DBUser
from DAL.DBPis import DBPis

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
CORS(app, resources={r"*": {"origins": [frontend_site,'https://python-frontend-obnagx4dh-smoothwin.vercel.app']}}
     , supports_credentials=True)
temperature = DBTemperature()
humidity = DBHumidity()
status = DBStatus()
pis = DBPis()

users = DBUser()


def response_create(message, code=200, delete_cookie = False):
    response_mod = make_response(message, code)
    if delete_cookie:
        response_mod.set_cookie("auth", value="", expires=0, path="/", httponly=True,
                            secure=True, samesite="None")
    return response_mod


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
            response={"message":"registration empty"},
            status=401,
            mimetype='application/json'
        )
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    exists = users.insert_user(new_user.public_id,new_user.name, new_user.password, new_user.admin)
    if exists is False:
        return app.response_class(
            response={"message":"user already exists"},
            status=401,
            mimetype='application/json'
        )
    return app.response_class(
            response={"message":"registered successfully"},
            status=201,
            mimetype='application/json'
        )
@app.route('/logout', methods=['post'])
def logout_user():
    if request.cookies.get("auth"):
        response = response_create({"message":"Logged in"}, delete_cookie=True)
        return response
    return response_create({"message":"Already logged out"}, 400)




@app.route('/login', methods=['post'])
def login_user():
    if request.cookies.get("auth"):
        values = decode_token(request.cookies.get("auth"))
        if values is None:
            response1 = response_create({"message":"invalid login (expired)"}, code=201, delete_cookie=True)
            return response1
        if values['admin'] is True:

            response1 = response_create({"message":"already authorized"}, 200)
        return response1
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return app.response_class(
            response={"message":"login required"},
            status=401,
            mimetype='application/json'
        )
    user = users.select_user(auth.username)
    # print(user)
    if user is None:
        return app.response_class(
            response={"message":"user doesn't exist"},
            status=401,
            mimetype='application/json',
        )
    # print(user['password'])
    if check_password_hash(user['password'], auth.password):
        token = jwt.encode({'public_id':user['uuid'], 'admin': user['admin'], 'exp':datetime.datetime.utcnow()+datetime.timedelta(
            # seconds=10, #more for debugging
            minutes=30,
        )},
                           os.environ.get("JWT_SECRET"), algorithm='HS256')
        response = response_create({"message":"authenticated"}, 200)
        response.set_cookie("auth", value=str(token), max_age=60*60*24*365*1, path="/", httponly=True
                            ,samesite="None", secure=True)

        return response

    return app.response_class(
            response={"wrong credentials"},
            status=401,
            mimetype='application/json',
        )
@app.route('/api/pies', methods=["GET"])
def get_all_pis():
    token = request.cookies.get("auth")
    if token is None:
        response = response_create({"message": "missing values"}, 404, delete_cookie=True)
        return response
    values = decode_token(token)
    if values is None:
        return response_create({"message": "Unauthorized"}, code=401, delete_cookie=True)
    if values['admin'] is False:
        response = response_create({"message": "Unauthorized"}, 401, True)
        return response

    all_pi = pis.select_all_pis()
    return make_response(json.dumps({"pies": all_pi}), 200)


@app.route('/', methods=["GET"])
def get_all_data():  # put application's code here

    token = request.cookies.get("auth")
    if token is None:
        response = response_create({"message":"missing values"}, 404, delete_cookie=True)
        return response
    values = decode_token(token)
    if values is None:

        return response_create({"message":"Unauthorized"}, code=401, delete_cookie=True)
    if values['admin'] is False:
        response = response_create({"message":"Unauthorized"}, 401, True)
        return response

    if request.args.get("pi"):
        all_temp = temperature.select_all_temperatures(request.args.get("pi"))
        all_hum = humidity.select_all_humidities(request.args.get("pi"))
        all_stat = status.select_all_status(request.args.get("pi"))

        response = app.response_class(
            response=json.dumps({"temperatures": all_temp, "humidities": all_hum, "status": all_stat}),
            status=200,
            mimetype='application/json'
        )
        return response
    return response_create({"message": "No pies specified"}, code=400)


@app.route('/api/send', methods = ['POST'])
def send_data():
    header_security = request.headers['security-check']
    content = request.json
    string = ""
    for i in content.keys():
        string += str(content[i])
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
    return make_response({"message":"Server online"}, 200)


if __name__ == '__main__':
    app.run()
