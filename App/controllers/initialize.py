from App.database import db
from App.models.user import User, Amenity

def create_user(username, email, password, user_type='tenant'):
    user = User(username=username, email=email, password=password, user_type=user_type)
    db.session.add(user)
    db.session.commit()
    return user

def create_amenities():
    """Create default amenities for apartment listings"""
    amenities = [
        {'name': 'Air Conditioning', 'icon': 'fa-snowflake'},
        {'name': 'Heating', 'icon': 'fa-fire'},
        {'name': 'Washer & Dryer', 'icon': 'fa-tshirt'},
        {'name': 'Parking', 'icon': 'fa-car'},
        {'name': 'Gym', 'icon': 'fa-dumbbell'},
        {'name': 'Pool', 'icon': 'fa-swimming-pool'},
        {'name': 'Dishwasher', 'icon': 'fa-sink'},
        {'name': 'Pet Friendly', 'icon': 'fa-paw'},
        {'name': 'Balcony', 'icon': 'fa-mountain'},
        {'name': 'Elevator', 'icon': 'fa-sort-amount-up-alt'},
        {'name': 'Security System', 'icon': 'fa-shield-alt'},
        {'name': 'Furnished', 'icon': 'fa-couch'}
    ]
    
    for amenity in amenities:
        existing = Amenity.query.filter_by(name=amenity['name']).first()
        if not existing:
            db.session.add(Amenity(name=amenity['name'], icon=amenity['icon']))
    
    db.session.commit()

def initialize():
    """Initialize the database with required data"""
    db.create_all()
    
    # Create admin user
    admin = User.query.filter_by(email='admin@apartmentreviews.com').first()
    if not admin:
        create_user('admin', 'admin@apartmentreviews.com', 'adminpass', 'admin')
    
    # Create amenities
    create_amenities()
