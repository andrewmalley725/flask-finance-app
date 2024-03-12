from flask import jsonify, request, Blueprint
from db import users
from bson import ObjectId

category_routes = Blueprint('category_routes', __name__)

@category_routes.route('/categories/<uid>', methods=['GET'])
def get_categories(uid):
    id = ObjectId(uid)
    user = users.find_one({'_id': id})
    categories = user['accounts']
    payload = {
        '_id': str(id),
        'username': user['username'],
        'accounts': categories,
        'total_balance': user['balance']
    }
    return payload

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
