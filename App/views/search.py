from flask import Blueprint
from App.controllers.search import search_bp

search_views = Blueprint('search_views', __name__, template_folder='../templates')

# Register the search Blueprint
def register_search_blueprint(app):
    # Register the views blueprint only, the controller blueprint is registered in main.py
    app.register_blueprint(search_views)