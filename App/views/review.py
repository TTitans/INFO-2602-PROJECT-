from flask import Blueprint
from App.controllers.review import review_bp

review_views = Blueprint('review_views', __name__, template_folder='../templates')

# Register the review Blueprint
def register_review_blueprint(app):
    # Register the views blueprint only, the controller blueprint is registered in main.py
    app.register_blueprint(review_views)