from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from flask_jwt_extended import jwt_required, unset_jwt_cookies, set_access_cookies

from App.controllers.auth import login, auth_bp
from App.models.user import User
from App.forms import LoginForm, RegistrationForm
from App.database import db

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

# Register the auth Blueprint
def register_auth_blueprint(app):
    # Register the controllers blueprint with a unique name to avoid conflicts
    app.register_blueprint(auth_bp, name='auth_controller')
    # Register the views blueprint
    app.register_blueprint(auth_views)

'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
    return render_template('message.html', title="Identify", 
                          message=f"You are logged in as {current_user.id} - {current_user.username}")

@auth_views.route('/login', methods=['GET', 'POST'])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for('index_views.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth_views.login_view'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('index_views.index')
        flash('Login successful!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form, title='Login')

@auth_views.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index_views.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            user_type=form.user_type.data
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth_views.login_view'))
    
    return render_template('auth/register.html', form=form, title='Register')

@auth_views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index_views.index'))

@auth_views.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', title='Profile')

'''
API Routes
'''
@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    token = login(data['email'], data['password'])
    if not token:
        return jsonify(message='Invalid email or password'), 401
    response = jsonify(access_token=token) 
    set_access_cookies(response, token)
    return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({
        'message': f"username: {current_user.username}, email: {current_user.email}, id: {current_user.id}"
    })

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response