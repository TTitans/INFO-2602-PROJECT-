from datetime import datetime
from sqlalchemy import Integer, Float, String, Text, Boolean, DateTime, ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

# Association table for listing_amenities (many-to-many)
listing_amenities = db.Table('listing_amenities',
    db.Column('listing_id', db.Integer, db.ForeignKey('listing.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenity.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    """User model representing landlords and tenants"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'landlord' or 'tenant'
    is_verified = db.Column(db.Boolean, default=False)  # For tenants verification
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    listings = db.relationship('Listing', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __init__(self, username, email, password, user_type):
        self.username = username
        self.email = email
        self.user_type = user_type
        self.is_verified = user_type == 'landlord'  # Auto-verify landlords for now
        self.set_password(password)

    def get_json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'user_type': self.user_type}

    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Listing(db.Model):
    """Apartment listings created by landlords"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable=False)
    square_feet = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='listing', lazy=True, cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=listing_amenities, lazy='subquery',
                               backref=db.backref('listings', lazy=True))

    def __repr__(self):
        return f'<Listing {self.title}>'

    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'square_feet': self.square_feet,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'created_at': self.created_at,
            'average_rating': self.average_rating()
        }


class Amenity(db.Model):
    """Amenities that can be associated with apartment listings"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(100), nullable=False)  # Font Awesome icon class

    def __repr__(self):
        return f'<Amenity {self.name}>'


class Review(db.Model):
    """Reviews written by verified tenants"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 star rating
    pros = db.Column(db.Text)
    cons = db.Column(db.Text)
    lease_period = db.Column(db.String(100))  # When they lived there
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Review {self.id} for Listing {self.listing_id}>'


class Admin(User):
    __tablename__ = 'admin'
    staff_id = db.Column(db.String(120), unique=True)
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }
