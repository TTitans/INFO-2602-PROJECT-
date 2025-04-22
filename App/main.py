import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from dotenv import load_dotenv

load_dotenv()

from App.database import init_db, db
from App.config import load_config
from App.models.user import User

# Import blueprints from controllers
from App.controllers.auth import auth_bp, setup_jwt, add_auth_context
from App.controllers.listing import listing_bp
from App.controllers.review import review_bp
from App.controllers.search import search_bp
from App.controllers.initialize import initialize

# Import legacy views
from App.views import views, setup_admin
from App.views.index import index_views
from App.views.auth import auth_views, register_auth_blueprint
from App.views.listing import listing_views, register_listing_blueprint
from App.views.review import review_views, register_review_blueprint
from App.views.search import search_views, register_search_blueprint

def add_views(app):
    # Register legacy views
    for view in views:
        app.register_blueprint(view)
    
    # Register views that use the controllers with unique names
    # These functions register the controller blueprints
    register_auth_blueprint(app)
    
    # Register listing_bp with a unique name
    app.register_blueprint(listing_bp, name='listing_controller')
    # Register the listing views blueprint
    register_listing_blueprint(app)
    
    # Register review_bp with a unique name
    app.register_blueprint(review_bp, name='review_controller')
    # Register the review views blueprint
    register_review_blueprint(app)
    
    # Register search_bp with a unique name
    app.register_blueprint(search_bp, name='search_controller')
    # Register the search views blueprint
    register_search_blueprint(app)

def setup_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_views.login_view'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        if user_id is not None:
            try:
                return User.query.get(int(user_id))
            except (ValueError, TypeError):
                return None
        return None
    
    return login_manager

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    
    # Set secret key
    app.secret_key = os.environ.get("SESSION_SECRET", "apartment-reviews-secret-key")
    
    # Configure database with fallback to SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///temp-database.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    CORS(app)
    init_db(app)
    # Removed duplicate initialization: db.init_app(app)
    
    # Setup authentication
    add_auth_context(app)
    jwt = setup_jwt(app)
    login_manager = setup_login_manager(app)
    
    # Setup upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register views
    add_views(app)
    setup_admin(app)
    
    # Error handling
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    # Create app context
    app.app_context().push()
    with app.app_context():
        # Initialize database if it doesn't exist
        db.create_all()
        
        # Create initial data
        initialize()
    
    return app

