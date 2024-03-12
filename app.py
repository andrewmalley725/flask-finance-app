from flask import Flask, request
from auth import validate_api_key
from routes import main_routes

app = Flask(__name__)
    
@app.before_request
def before_request():
    whitelist_routes = ['main_routes.user_routes.auth', 'main_routes.user_routes.add_user']
    if request.endpoint and request.endpoint not in whitelist_routes:
        return validate_api_key()
    
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
