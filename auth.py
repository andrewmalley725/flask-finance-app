from flask import request, jsonify
import os

def validate_api_key():
    api_key = request.headers.get('x-api-key')
    if api_key != os.environ.get('API_KEY'):
        response = jsonify({"error": "Invalid API key"})
        response.status_code = 401
        return response