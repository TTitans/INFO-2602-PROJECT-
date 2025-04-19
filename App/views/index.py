from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from sqlalchemy import desc
from App.controllers.initialize import initialize
from App.models.user import Listing, User
from App.forms import SearchForm

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index():
    """Home page with featured listings and search form"""
    # Get latest listings for featured section
    featured_listings = Listing.query.order_by(desc(Listing.created_at)).limit(6).all()
    
    # Initialize search form
    search_form = SearchForm()
    
    # Get some stats for the home page
    total_listings = Listing.query.count()
    total_landlords = User.query.filter_by(user_type='landlord').count()
    total_tenants = User.query.filter_by(user_type='tenant').count()
    
    return render_template('home.html', 
                          featured_listings=featured_listings,
                          search_form=search_form,
                          total_listings=total_listings,
                          total_landlords=total_landlords,
                          total_tenants=total_tenants,
                          title='Apartment Reviews')

@index_views.route('/init', methods=['GET'])
def init():
    """Initialize the database with required data"""
    initialize()
    return jsonify(message='Database initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({'status':'healthy'})
