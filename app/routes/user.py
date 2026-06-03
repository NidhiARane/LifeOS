"""
User Routes
Handles user profile management, settings, and account operations
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.user import User
from app.utils.validators import validate_email
from app.services.analytics_service import AnalyticsService

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/profile')
@login_required
def profile():
    """View user profile"""
    return render_template('user/profile.html', user=current_user, show_back_button=True)


@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    if request.method == 'POST':
        data = request.form

        # Update profile information
        current_user.first_name = data.get('first_name', '').strip()
        current_user.last_name = data.get('last_name', '').strip()
        current_user.bio = data.get('bio', '').strip()
        current_user.phone = data.get('phone', '').strip()
        current_user.location = data.get('location', '').strip()

        # Update monthly budget if provided and sync to UserBudget
        mb_value = data.get('monthly_budget')
        if mb_value:
            try:
                current_user.monthly_budget = float(mb_value)
            except ValueError:
                flash('Invalid budget amount!', 'error')
                return redirect(url_for('user.edit_profile'))

            # Also sync to UserBudget model to keep both sources synchronized
            try:
                budget = AnalyticsService.get_or_create_budget(current_user.id, monthly_limit=current_user.monthly_budget)
                budget.monthly_limit = current_user.monthly_budget
                budget.updated_at = datetime.utcnow()
                db.session.add(budget)
            except Exception:
                try:
                    from flask import current_app
                    current_app.logger.exception('Failed to sync UserBudget in edit_profile')
                except Exception:
                    pass

        # Other numeric goal updates
        if data.get('weight_goal'):
            try:
                current_user.weight_goal = float(data.get('weight_goal'))
            except ValueError:
                flash('Invalid weight goal!', 'error')
                return redirect(url_for('user.edit_profile'))

        if data.get('savings_goal'):
            try:
                current_user.savings_goal = float(data.get('savings_goal'))
            except ValueError:
                flash('Invalid savings goal!', 'error')
                return redirect(url_for('user.edit_profile'))

        if data.get('daily_calorie_goal'):
            try:
                current_user.daily_calorie_goal = int(data.get('daily_calorie_goal'))
            except ValueError:
                flash('Invalid calorie goal!', 'error')
                return redirect(url_for('user.edit_profile'))

        if data.get('daily_protein_goal'):
            try:
                current_user.daily_protein_goal = float(data.get('daily_protein_goal'))
            except ValueError:
                flash('Invalid protein goal!', 'error')
                return redirect(url_for('user.edit_profile'))

        # Commit all changes once (user fields + budget)
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.profile'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update profile!', 'error')
            return redirect(url_for('user.edit_profile'))

    return render_template('user/edit_profile.html', user=current_user)


@user_bp.route('/settings')
@login_required
def settings():
    """User settings page"""
    return render_template('user/settings.html', user=current_user, show_back_button=True)


@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    if request.method == 'POST':
        data = request.form
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')

        # Verify old password
        if not current_user.check_password(old_password):
            flash('Current password is incorrect!', 'error')
            return redirect(url_for('user.change_password'))

        # Validate new password
        if len(new_password) < 8:
            flash('Password must be at least 8 characters!', 'error')
            return redirect(url_for('user.change_password'))

        if new_password != confirm_password:
            flash('New passwords do not match!', 'error')
            return redirect(url_for('user.change_password'))

        # Update password
        current_user.set_password(new_password)
        try:
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('user.settings'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to change password!', 'error')
            return redirect(url_for('user.change_password'))

    return render_template('user/change_password.html', show_back_button=True)


@user_bp.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    """Delete user account"""
    if request.method == 'POST':
        password = request.form.get('password', '')

        # Verify password
        if not current_user.check_password(password):
            flash('Password is incorrect!', 'error')
            return redirect(url_for('user.delete_account'))

        try:
            user_id = current_user.id
            db.session.delete(current_user)
            db.session.commit()
            flash('Your account has been deleted!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to delete account!', 'error')
            return redirect(url_for('user.delete_account'))

    return render_template('user/delete_account.html', show_back_button=True)


@user_bp.route('/api/profile', methods=['GET'])
@login_required
def api_get_profile():
    """API endpoint to get user profile"""
    return jsonify(current_user.to_dict())


@user_bp.route('/api/profile', methods=['PUT'])
@login_required
def api_update_profile():
    """API endpoint to update user profile"""
    data = request.get_json() or {}

    # Update allowed fields
    if 'first_name' in data:
        current_user.first_name = data['first_name']
    if 'last_name' in data:
        current_user.last_name = data['last_name']
    if 'bio' in data:
        current_user.bio = data['bio']
    if 'phone' in data:
        current_user.phone = data['phone']
    if 'location' in data:
        current_user.location = data['location']
    if 'monthly_budget' in data:
        try:
            current_user.monthly_budget = float(data['monthly_budget'])
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid monthly_budget value'}), 400

        # Also sync to UserBudget model when budget is updated via API
        try:
            budget = AnalyticsService.get_or_create_budget(current_user.id, monthly_limit=current_user.monthly_budget)
            budget.monthly_limit = current_user.monthly_budget
            budget.updated_at = datetime.utcnow()
            db.session.add(budget)
        except Exception:
            try:
                from flask import current_app
                current_app.logger.exception('Failed to sync UserBudget in api_update_profile')
            except Exception:
                pass

    if 'weight_goal' in data:
        try:
            current_user.weight_goal = float(data['weight_goal'])
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid weight_goal value'}), 400
    if 'savings_goal' in data:
        try:
            current_user.savings_goal = float(data['savings_goal'])
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid savings_goal value'}), 400
    if 'daily_calorie_goal' in data:
        try:
            current_user.daily_calorie_goal = int(data['daily_calorie_goal'])
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid daily_calorie_goal value'}), 400
    if 'daily_protein_goal' in data:
        try:
            current_user.daily_protein_goal = float(data['daily_protein_goal'])
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid daily_protein_goal value'}), 400

    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully', 'user': current_user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update profile', 'error': str(e)}), 400

