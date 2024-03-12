from flask import Blueprint
from routes.user_routes import user_routes
from routes.category_routes import category_routes

main_routes = Blueprint('main_routes', __name__)
main_routes.register_blueprint(user_routes)
main_routes.register_blueprint(category_routes)

