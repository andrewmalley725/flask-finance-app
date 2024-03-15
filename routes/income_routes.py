from flask import jsonify, request, Blueprint
from flask_cors import CORS
from db import users
from bson import ObjectId
from datetime import datetime


income_routes = Blueprint('income_routes', __name__)
CORS(income_routes)

@income_routes.route('/addPayday/<uid>', methods=['POST'])
def add_income(uid):
    id = ObjectId(uid)
    user = users.find_one({'_id': id})

    current_datetime = datetime.now()
    date_time_stamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    body = request.json
    body['date'] = date_time_stamp
    total_balance = user['balance'] + body['amount']
    operations = {
        '$push': {'income': body},
        '$set': {'balance': total_balance}
    }
    users.update_one({'_id': id}, operations)

    for i in range(len(user['accounts'])):
        account = user['accounts'][i]
        new_balance = account['weight'] * total_balance
        users.update_one({'_id': id}, {'$set': {f'accounts.{i}.balance': new_balance}})

    user = users.find_one({'_id':id})
    user['_id'] = str(user['_id'])
    del user['password']

    return jsonify({'status': 'added', 'user': user})

