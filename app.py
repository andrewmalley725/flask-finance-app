from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
import certifi
from bson import ObjectId
import creds

uri = creds.MOGO_URI
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client['finance-app']
users = db.user

app = Flask(__name__)

def validate_api_key():
    api_key = request.headers.get('x-api-key')
    if api_key != creds.API_KEY:
        response = jsonify({"error": "Invalid API key"})
        response.status_code = 401
        return response
    
@app.before_request
def before_request():
    whitelist_routes = ['auth']
    if request.endpoint and request.endpoint not in whitelist_routes:
        return validate_api_key()

@app.route('/users', methods=['GET'])
def get_users():
    data = list(users.find())
    result = []
    for user in data:
        record = {}
        record['_id'] = str(user['_id'])
        record['username'] = user['username']
        record['firstname'] = user['firstname']
        record['lastname'] = user['lastname']
        record['password'] = user['password']
        record['balance'] = user['balance']
        result.append(record)
    return jsonify(result)

@app.route('/authenticate', methods=['POST'])
def auth():
    msg = ''
    result = {}
    data = request.json
    username = data['username']
    password = data['password']
    user = users.find_one({'username':username})
    if user:
        if password == user['password']:
            msg = 'successfully logged in'
            result['_id'] = str(user['_id'])
            result['name'] = f'{user["firstname"]} {user["lastname"]}'
            result['username'] = user['username']
            result['apiKey'] = creds.API_KEY
        else:
            msg = 'invalid password'
    else:
        msg = 'please enter a valid username'
    result['status'] = msg
    return result

if __name__ == '__main__':
    app.run(debug=True)
