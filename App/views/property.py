
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from App.controllers import (
    create_property,
    get_property,
    get_all_properties,
    search_properties,
    create_review
)

property_views = Blueprint('property_views', __name__, template_folder='../templates')

@property_views.route('/properties', methods=['GET'])
def get_properties():
    city = request.args.get('city')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    rooms = request.args.get('rooms', type=int)
    furnished = request.args.get('furnished', type=bool)
    
    if any([city, min_price, max_price, rooms, furnished]):
        properties = search_properties(city, min_price, max_price, rooms, furnished)
    else:
        properties = get_all_properties()
    
    return render_template('properties.html', properties=properties)

@property_views.route('/properties/new', methods=['GET', 'POST'])
@jwt_required()
def create_property_page():
    if request.method == 'POST':
        property = create_property(
            title=request.form['title'],
            description=request.form['description'],
            price=float(request.form['price']),
            city=request.form['city'],
            address=request.form['address'],
            rooms=int(request.form['rooms']),
            bathrooms=int(request.form['bathrooms']),
            property_type=request.form['property_type'],
            area=float(request.form['area']),
            furnished=bool(request.form.get('furnished')),
            amenities=request.form['amenities'],
            landlord_id=current_user.id
        )
        flash('Property listing created successfully!')
        return redirect(url_for('property_views.get_properties'))
    return render_template('property_form.html')

@property_views.route('/properties/<int:id>', methods=['GET'])
def get_property_page(id):
    property = get_property(id)
    if not property:
        flash('Property not found')
        return redirect(url_for('property_views.get_properties'))
    return render_template('property_detail.html', property=property)

@property_views.route('/properties/<int:id>/review', methods=['POST'])
@jwt_required()
def create_review_action(id):
    review = create_review(
        rating=int(request.form['rating']),
        comment=request.form['comment'],
        property_id=id,
        tenant_id=current_user.id
    )
    flash('Review submitted successfully!')
    return redirect(url_for('property_views.get_property_page', id=id))
