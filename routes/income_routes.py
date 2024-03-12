from flask import jsonify, request, Blueprint
from db import users
from bson import ObjectId
from datetime import datetime


income_routes = Blueprint('income_routes', __name__)

@income_routes.route('/addPayday/<uid>', methods=['POST'])
def add_income(uid):
    id = ObjectId(uid)
    user = users.find_one({'_id': id})

    current_datetime = datetime.now()
    date_time_stamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    body = request.json
    body['date'] = date_time_stamp
    operations = {
        '$push': {'income': body},
        '$set': {'balance': user['balance'] + body['amount']}
    }
    users.update_one({'_id': id}, operations)

    for i in range(len(user['accounts'])):
        account = user['accounts'][i]
        new_balance = account['weight'] * body['amount']
        users.update_one({'_id': id}, {'$set': {f'accounts.{i}.balance': new_balance}})

    return jsonify({'status': 'added'})

