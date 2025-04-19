from sqlalchemy import Integer
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return {'id': self.id, 'username': self.username}

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    property_type = db.Column(db.String(120), nullable=False)
    area = db.Column(db.Float, nullable=False)
    furnished = db.Column(db.Boolean, default=False)
    amenities = db.Column(db.Text, nullable=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    landlord = db.relationship('User', backref='properties')
    reviews = db.relationship('Review', backref='property', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'city': self.city,
            'address': self.address,
            'rooms': self.rooms,
            'bathrooms': self.bathrooms,
            'property_type': self.property_type,
            'area': self.area,
            'furnished': self.furnished,
            'amenities': self.amenities,
            'landlord': self.landlord.username
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tenant = db.relationship('User', backref='reviews')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def get_json(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'property_id': self.property_id,
            'tenant': self.tenant.username,
            'created_at': self.created_at
        }


class Admin(User):
    __tablename__ = 'admin'
    staff_id = db.Column(db.String(120), unique=True)
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }
