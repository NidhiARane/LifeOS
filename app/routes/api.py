"""
API Routes
RESTful API endpoints
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.user import User

api_bp = Blueprint('api', __name__)


@api_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    """Get all users (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@api_bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """Get user by ID"""
    if user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'LifeOS API is running'})

