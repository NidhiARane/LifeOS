"""
Authentication Routes
Handles user registration, login, logout, and password management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.utils.validators import validate_email, validate_password
from app.utils.decorators import anonymous_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
@anonymous_required
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.form

        # Validation
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')

        # Check for existing user
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
            return redirect(url_for('auth.register'))

        # Validate email
        if not validate_email(email):
            flash('Invalid email format!', 'error')
            return redirect(url_for('auth.register'))

        # Validate password
        if not validate_password(password):
            flash('Password must be at least 8 characters with uppercase, lowercase, and number!', 'error')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.register'))

        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=data.get('first_name', '').strip(),
            last_name=data.get('last_name', '').strip()
        )
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
    """User login"""
    if request.method == 'POST':
        data = request.form
        username = data.get('username', '').strip()
        password = data.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password!', 'error')
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash('Your account has been deactivated!', 'error')
            return redirect(url_for('auth.login'))

        # Login user
        login_user(user, remember=data.get('remember_me'))
        user.update_last_login()

        flash(f'Welcome back, {user.get_full_name()}!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
@anonymous_required
def forgot_password():
    """Password reset request"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = User.query.filter_by(email=email).first()

        if user:
            # TODO: Implement password reset token and email
            flash('If an account exists with this email, you will receive password reset instructions.', 'info')
        else:
            flash('If an account exists with this email, you will receive password reset instructions.', 'info')

        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')

