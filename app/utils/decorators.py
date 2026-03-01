"""
Decorators
Custom decorators for routes and functions
"""
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def anonymous_required(f):
    """
    Decorator to ensure user is NOT logged in
    Redirects to dashboard if already logged in
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorator to ensure user is admin
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))

        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.dashboard'))

        return f(*args, **kwargs)
    return decorated_function


def require_json(f):
    """
    Decorator to require JSON request
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify

        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        return f(*args, **kwargs)
    return decorated_function

