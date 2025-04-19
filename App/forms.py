from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, IntegerField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, ValidationError
from App.models.user import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('I am a', choices=[('tenant', 'Tenant'), ('landlord', 'Landlord')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ListingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Monthly Rent ($)', validators=[DataRequired(), NumberRange(min=0)])
    bedrooms = IntegerField('Bedrooms', validators=[DataRequired(), NumberRange(min=0)])
    bathrooms = FloatField('Bathrooms', validators=[DataRequired(), NumberRange(min=0)])
    square_feet = IntegerField('Square Feet', validators=[DataRequired(), NumberRange(min=0)])
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=50)])
    zip_code = StringField('ZIP Code', validators=[DataRequired(), Length(max=20)])
    amenities = SelectMultipleField('Amenities', coerce=int)
    submit = SubmitField('Create Listing')

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        from App.models.user import Amenity
        # Dynamically set the amenities choices
        self.amenities.choices = [(a.id, a.name) for a in Amenity.query.order_by(Amenity.name).all()]

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), 
                                          (4, '4 Stars'), (5, '5 Stars')], 
                        validators=[DataRequired()], coerce=int)
    content = TextAreaField('Review', validators=[DataRequired()])
    pros = TextAreaField('Pros')
    cons = TextAreaField('Cons')
    lease_period = StringField('When did you live here? (e.g., Jan 2020 - Dec 2021)', validators=[DataRequired()])
    submit = SubmitField('Submit Review')

class SearchForm(FlaskForm):
    location = StringField('City, State, or ZIP')
    min_price = FloatField('Min Price', validators=[], default=0)
    max_price = FloatField('Max Price', validators=[])
    bedrooms = SelectField('Bedrooms', choices=[
        ('', 'Any'),
        (1, '1+'),
        (2, '2+'),
        (3, '3+'),
        (4, '4+')
    ], coerce=int, default='')
    bathrooms = SelectField('Bathrooms', choices=[
        ('', 'Any'),
        (1, '1+'),
        (1.5, '1.5+'),
        (2, '2+'),
        (3, '3+')
    ], coerce=float, default='')
    amenities = SelectMultipleField('Amenities', coerce=int)
    submit = SubmitField('Search')

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        from App.models.user import Amenity
        # Dynamically set the amenities choices
        self.amenities.choices = [(a.id, a.name) for a in Amenity.query.order_by(Amenity.name).all()]