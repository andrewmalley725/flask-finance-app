from flask import jsonify, request, Blueprint
from flask_cors import CORS
from db import users
from bson import ObjectId

category_routes = Blueprint('category_routes', __name__)
CORS(category_routes)

@category_routes.route('/addCategory/<uid>', methods=['POST'])
def add_category(uid):
    id = ObjectId(uid)
    user = users.find_one({'_id': id})
    unallocated = user['accounts'][0]['weight']

    body = request.json
    account_weight = body['weight']
    unallocated -= account_weight
    unallocated_balance = unallocated * user['balance']

    body['balance'] = user['balance'] * account_weight
    update_operations = {
        '$push': {'accounts': body},
    }
    users.update_one(user, update_operations)
    users.update_one({'_id': id}, {'$set': {'accounts.0.weight': unallocated, 'accounts.0.balance': unallocated_balance}})
    return jsonify({'status': 'success'})

@category_routes.route('/deleteCategory/<uid>', methods=['DELETE'])
def del_category(uid):
    user = users.find_one({'_id': ObjectId(uid)})
    unallocated_bal = user['accounts'][0]['balance']
    unallocated_weight = user['accounts'][0]['weight']
    category = request.args.get('category')
    for i in range(len(user['accounts'])):
        account = user['accounts'][i]
        if account['account_name'] == category:
            balance = account['balance']
            weight = account['weight']
            users.update_one({'_id': ObjectId(uid)}, {'$set': {'accounts.0.balance': unallocated_bal + balance, 'accounts.0.weight': unallocated_weight + weight}})
            users.update_one({'_id': ObjectId(uid)}, {'$pull': {'accounts': {'account_name': category}}})
            return jsonify({'status':'success'})
    return jsonify({'status':'account does not exist'})

