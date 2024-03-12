from flask import request, jsonify
import creds

def validate_api_key():
    api_key = request.headers.get('x-api-key')
    if api_key != creds.API_KEY:
        response = jsonify({"error": "Invalid API key"})
        response.status_code = 401
        return response