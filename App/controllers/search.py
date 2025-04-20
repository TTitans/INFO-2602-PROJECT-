
from flask import Blueprint, render_template, request
from sqlalchemy import or_
from App.models.user import Listing, Amenity
from App.forms import SearchForm

search_bp = Blueprint('search_controller', __name__, url_prefix='/search')

@search_bp.route('/', methods=['GET'])
def search():
    """Search for apartment listings based on criteria"""
    from App.controllers.initialize import initialize
    initialize()  # Ensure amenities exist
    
    form = SearchForm(request.args, meta={'csrf': False})
    
    query = Listing.query
    
    # Apply filters if provided
    if form.location.data:
        search_term = f"%{form.location.data}%"
        query = query.filter(or_(
            Listing.city.ilike(search_term),
            Listing.state.ilike(search_term),
            Listing.zip_code.ilike(search_term)
        ))
    
    if form.min_price.data is not None:
        query = query.filter(Listing.price >= form.min_price.data)
    
    if form.max_price.data is not None:
        query = query.filter(Listing.price <= form.max_price.data)
    
    if form.bedrooms.data:
        query = query.filter(Listing.bedrooms >= form.bedrooms.data)
    
    if form.bathrooms.data:
        query = query.filter(Listing.bathrooms >= form.bathrooms.data)
    
    # Filter by amenities (if selected)
    if form.amenities.data:
        for amenity_id in form.amenities.data:
            query = query.filter(Listing.amenities.any(Amenity.id == amenity_id))
    
    # Get all amenities for the form
    amenities = Amenity.query.all()
    form.amenities.choices = [(str(a.id), a.name) for a in amenities]
    
    # Get search results
    results = query.order_by(Listing.created_at.desc()).all()
    
    return render_template('listings/search.html', 
                         form=form, 
                         results=results, 
                         total=len(results),
                         amenities=amenities,
                         title='Search Results')
