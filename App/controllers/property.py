
from App.models import Property, Review
from App.database import db

def create_property(title, description, price, city, address, rooms, bathrooms, property_type, area, furnished, amenities, landlord_id):
    property = Property(
        title=title,
        description=description,
        price=price,
        city=city,
        address=address,
        rooms=rooms,
        bathrooms=bathrooms,
        property_type=property_type,
        area=area,
        furnished=furnished,
        amenities=amenities,
        landlord_id=landlord_id
    )
    db.session.add(property)
    db.session.commit()
    return property

def get_property(id):
    return Property.query.get(id)

def get_all_properties():
    return Property.query.all()

def search_properties(city=None, min_price=None, max_price=None, rooms=None, furnished=None):
    query = Property.query
    if city:
        query = query.filter(Property.city.ilike(f'%{city}%'))
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)
    if rooms:
        query = query.filter(Property.rooms == rooms)
    if furnished is not None:
        query = query.filter(Property.furnished == furnished)
    return query.all()

def create_review(rating, comment, property_id, tenant_id):
    review = Review(
        rating=rating,
        comment=comment,
        property_id=property_id,
        tenant_id=tenant_id
    )
    db.session.add(review)
    db.session.commit()
    return review
