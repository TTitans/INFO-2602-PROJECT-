from flask import Blueprint
from App.controllers.listing import listing_bp

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

# Register the listing Blueprint
def register_listing_blueprint(app):
    # Register the views blueprint only, the controller blueprint is registered in main.py
    app.register_blueprint(listing_views)