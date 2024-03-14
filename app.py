from flask import Flask, request
from auth import validate_api_key
from routes import main_routes
from flasgger import Swagger
import creds


app = Flask(__name__)
app.config['SWAGGER'] = {
    'openapi': '3.0.0'
}
swagger = Swagger(app, template_file='swagger.yaml')

@app.before_request
def before_request():
    print(request.endpoint)
    whitelist_routes = ['main_routes.user_routes.auth', 'main_routes.user_routes.add_user', 'main_routes.test', 'flasgger']
    if any(request.endpoint.startswith(pattern) for pattern in whitelist_routes):
        return
    return validate_api_key()
    
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
