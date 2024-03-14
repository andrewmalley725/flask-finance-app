from bson import ObjectId
from flask import jsonify, request, Blueprint
from flask_cors import CORS
from db import users
from hash import sha256_hash
from dotenv import load_dotenv
import os

load_dotenv()

user_routes = Blueprint('user_routes', __name__)
CORS(user_routes)

@user_routes.route('/data/<uid>', methods=['GET', 'OPTIONS'])
def get_data(uid):
    print('ping')
    user = users.find_one({'_id': ObjectId(uid)})
    user['_id'] = str(user['_id'])
    del user['password']
    return jsonify(user)

@user_routes.route('/addUser', methods=['POST'])
def add_user():
    body = request.json
    body['accounts'] = [{
        'account_name': 'Unallocated funds',
        'weight': 1.0,
        'balance': 0
    }]
    body['transactions'] = []
    body['income'] = []
    body['balance'] = 0.0
    body['password'] = sha256_hash(body['password'])
    id = users.insert_one(body).inserted_id
    return {
        '_id': str(id),
        'name': f'{body["firstname"]} {body["lastname"]}',
        'username': body['username'],
        'apiKey': os.getenv('API_KEY')
    }


@user_routes.route('/authenticate', methods=['POST'])
def auth():
    msg = ''
    result = {}
    data = request.json
    username = data['username']
    password = sha256_hash(data['password'])
    user = users.find_one({'username':username})
    if user:
        if password == user['password']:
            msg = 'successfully logged in'
            result['_id'] = str(user['_id'])
            result['name'] = f'{user["firstname"]} {user["lastname"]}'
            result['username'] = user['username']
            result['apiKey'] = os.getenv('API_KEY')
        else:
            msg = 'invalid password'
    else:
        msg = 'please enter a valid username'
    result['status'] = msg
    return result