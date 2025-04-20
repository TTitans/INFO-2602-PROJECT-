from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from App.database import db
from App.models.user import Listing, Amenity, User
from App.forms import ListingForm
from datetime import datetime

listing_bp = Blueprint('listing_controller', __name__, url_prefix='/listings')


@listing_bp.route('/')
def list_apartments():
    """View all apartment listings"""
    page = request.args.get('page', 1, type=int)
    listings = Listing.query.order_by(Listing.created_at.desc()).paginate(
        page=page, per_page=9)
    return render_template('listings/view.html',
                           listings=listings,
                           title='Apartments')


@listing_bp.route('/my-listings')
@login_required
def my_listings():
    """View listings created by the current user (landlord only)"""
    if current_user.user_type != 'landlord':
        flash('Only landlords can view their listings.', 'warning')
        return redirect(url_for('index_views.index'))

    listings = Listing.query.filter_by(owner_id=current_user.id).order_by(
        Listing.created_at.desc()).all()
    return render_template('listings/my_listings.html',
                           listings=listings,
                           title='My Listings')


@listing_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new apartment listing (landlord only)"""
    if current_user.user_type != 'landlord':
        flash('Only landlords can create listings.', 'warning')
        return redirect(url_for('index_views.index'))

    form = ListingForm()
    if form.validate_on_submit():
        listing = Listing(title=form.title.data,
                          description=form.description.data,
                          price=form.price.data,
                          bedrooms=form.bedrooms.data,
                          bathrooms=form.bathrooms.data,
                          square_feet=form.square_feet.data,
                          address=form.address.data,
                          city=form.city.data,
                          state=form.state.data,
                          zip_code=form.zip_code.data,
                          owner_id=current_user.id)

        # Add selected amenities
        if form.amenities.data:
            amenities = Amenity.query.filter(
                Amenity.id.in_(form.amenities.data)).all()
            listing.amenities = amenities

        db.session.add(listing)
        db.session.commit()

        flash('Listing created successfully!', 'success')
        return redirect(url_for('listing.detail', apartment_id=listing.id))

    return render_template('listings/create.html',
                           form=form,
                           title='Create Listing')


@listing_bp.route('/<int:apartment_id>')
def detail(apartment_id):
    """View details of a specific apartment listing"""
    listing = Listing.query.get_or_404(apartment_id)
    return render_template('listings/detail.html',
                           listing=listing,
                           title=listing.title)


@listing_bp.route('/<int:apartment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(apartment_id):
    """Edit an existing apartment listing (owner only)"""
    listing = Listing.query.get_or_404(apartment_id)

    # Check if the current user is the owner
    if listing.owner_id != current_user.id:
        flash('You can only edit your own listings.', 'danger')
        return redirect(url_for('listing.detail', apartment_id=listing.id))

    form = ListingForm(obj=listing)
    if form.validate_on_submit():
        listing.title = form.title.data
        listing.description = form.description.data
        listing.price = form.price.data
        listing.bedrooms = form.bedrooms.data
        listing.bathrooms = form.bathrooms.data
        listing.square_feet = form.square_feet.data
        listing.address = form.address.data
        listing.city = form.city.data
        listing.state = form.state.data
        listing.zip_code = form.zip_code.data
        listing.updated_at = datetime.utcnow()

        # Update amenities
        if form.amenities.data:
            amenities = Amenity.query.filter(
                Amenity.id.in_(form.amenities.data)).all()
            listing.amenities = amenities
        else:
            listing.amenities = []

        db.session.commit()

        flash('Listing updated successfully!', 'success')
        return redirect(url_for('listing.detail', apartment_id=listing.id))

    # Pre-select the current amenities
    form.amenities.data = [amenity.id for amenity in listing.amenities]

    return render_template('listings/edit.html',
                           form=form,
                           listing=listing,
                           title='Edit Listing')


@listing_bp.route('/<int:apartment_id>/delete', methods=['POST'])
@login_required
def delete(apartment_id):
    """Delete an apartment listing (owner only)"""
    listing = Listing.query.get_or_404(apartment_id)

    # Check if the current user is the owner
    if listing.owner_id != current_user.id:
        flash('You can only delete your own listings.', 'danger')
        return redirect(url_for('listing.detail', apartment_id=listing.id))

    db.session.delete(listing)
    db.session.commit()

    flash('Listing deleted successfully.', 'success')
    return redirect(url_for('listing.my_listings'))
