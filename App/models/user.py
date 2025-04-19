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
    description = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(120), nullable=False)
    property_type = db.Column(db.String(120), nullable=False)
    LandArea = db.Column(db.Integer, nullable=False)
    floorArea = db.Column(db.Integer, nullable=False)
    furnish = db.Column(db.Boolean, default=False)


class Admin(User):
    __tablename__ = 'admin'
    staff_id = db.Column(db.String(120), unique=True)
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }
