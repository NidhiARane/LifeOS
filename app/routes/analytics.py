"""
Analytics Routes
Handles analytics, dashboard, and Life Score calculations
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.analytics import LifeScore, UserBudget
from app.services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')


# ==================== DASHBOARD ROUTES ====================

@analytics_bp.route('/dashboard')
@login_required
def dashboard():
    """Display main analytics dashboard"""
    try:
        dashboard_data = AnalyticsService.get_dashboard_data(current_user.id)

        return render_template('analytics/dashboard.html', **dashboard_data)

    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return redirect(url_for('main.index'))


# ==================== LIFE SCORE ROUTES ====================

@analytics_bp.route('/life-score')
@login_required
def life_score_dashboard():
    """Display Life Score and component scores"""
    try:
        life_score_data = AnalyticsService.calculate_life_score(current_user.id)

        return render_template('analytics/life_score.html', life_score=life_score_data)

    except Exception as e:
        flash(f'Error loading Life Score: {str(e)}', 'danger')
        return redirect(url_for('analytics.dashboard'))


# ==================== EXPENSE ANALYTICS ROUTES ====================

@analytics_bp.route('/expenses')
@login_required
def expenses_analytics():
    """Display expense analytics"""
    try:
        days = request.args.get('days', 30, type=int)
        expense_summary = AnalyticsService.get_expense_summary(current_user.id, days)
        daily_expenses = AnalyticsService.get_daily_expenses(current_user.id, days)
        category_breakdown = AnalyticsService.get_category_breakdown(current_user.id, days)

        return render_template('analytics/expenses.html',
                              expense_summary=expense_summary,
                              daily_expenses=daily_expenses,
                              category_breakdown=category_breakdown,
                              selected_days=days)

    except Exception as e:
        flash(f'Error loading expense analytics: {str(e)}', 'danger')
        return redirect(url_for('analytics.dashboard'))


# ==================== HEALTH ANALYTICS ROUTES ====================

@analytics_bp.route('/health')
@login_required
def health_analytics():
    """Display health analytics"""
    try:
        days = request.args.get('days', 30, type=int)
        health_summary = AnalyticsService.get_health_summary(current_user.id, days)
        daily_calories = AnalyticsService.get_daily_calories(current_user.id, days)

        return render_template('analytics/health.html',
                              health_summary=health_summary,
                              daily_calories=daily_calories,
                              selected_days=days)

    except Exception as e:
        flash(f'Error loading health analytics: {str(e)}', 'danger')
        return redirect(url_for('analytics.dashboard'))


# ==================== HABIT ANALYTICS ROUTES ====================

@analytics_bp.route('/habits')
@login_required
def habits_analytics():
    """Display habit analytics"""
    try:
        habit_progress = AnalyticsService.get_habit_progress(current_user.id)

        return render_template('analytics/habits.html', habit_progress=habit_progress)

    except Exception as e:
        flash(f'Error loading habit analytics: {str(e)}', 'danger')
        return redirect(url_for('analytics.dashboard'))


# ==================== BUDGET MANAGEMENT ROUTES ====================

@analytics_bp.route('/budget', methods=['GET', 'POST'])
@login_required
def manage_budget():
    """Manage user budget settings"""
    try:
        budget = AnalyticsService.get_or_create_budget(current_user.id)

        if request.method == 'POST':
            monthly_limit = float(request.form.get('monthly_limit', budget.monthly_limit))
            alert_threshold = float(request.form.get('alert_threshold', budget.alert_threshold))

            budget.monthly_limit = monthly_limit
            budget.alert_threshold = alert_threshold
            budget.updated_at = datetime.utcnow()

            # Keep the user's profile monthly_budget synchronized with the UserBudget
            try:
                # current_user is the logged-in User instance provided by flask-login
                current_user.monthly_budget = monthly_limit
            except Exception:
                # If for some reason current_user is not available or assignment fails,
                # proceed with committing the budget change only to avoid blocking users.
                pass

            db.session.commit()
            flash('Budget updated successfully!', 'success')
            return redirect(url_for('analytics.dashboard'))

        return render_template('analytics/budget.html', budget=budget)

    except Exception as e:
        db.session.rollback()
        flash(f'Error updating budget: {str(e)}', 'danger')
        return redirect(url_for('analytics.manage_budget'))


# ==================== API ROUTES ====================

@analytics_bp.route('/api/life-score', methods=['GET'])
@login_required
def get_life_score_api():
    """Get Life Score data (API)"""
    life_score_data = AnalyticsService.calculate_life_score(current_user.id)
    return jsonify(life_score_data)


@analytics_bp.route('/api/expense-summary', methods=['GET'])
@login_required
def get_expense_summary_api():
    """Get expense summary (API)"""
    days = request.args.get('days', 30, type=int)
    summary = AnalyticsService.get_expense_summary(current_user.id, days)
    return jsonify(summary)


@analytics_bp.route('/api/health-summary', methods=['GET'])
@login_required
def get_health_summary_api():
    """Get health summary (API)"""
    days = request.args.get('days', 30, type=int)
    summary = AnalyticsService.get_health_summary(current_user.id, days)
    return jsonify(summary)


@analytics_bp.route('/api/daily-expenses', methods=['GET'])
@login_required
def get_daily_expenses_api():
    """Get daily expense data (API)"""
    days = request.args.get('days', 30, type=int)
    data = AnalyticsService.get_daily_expenses(current_user.id, days)
    return jsonify(data)


@analytics_bp.route('/api/daily-calories', methods=['GET'])
@login_required
def get_daily_calories_api():
    """Get daily calorie data (API)"""
    days = request.args.get('days', 30, type=int)
    data = AnalyticsService.get_daily_calories(current_user.id, days)
    return jsonify(data)


@analytics_bp.route('/api/category-breakdown', methods=['GET'])
@login_required
def get_category_breakdown_api():
    """Get category breakdown (API)"""
    days = request.args.get('days', 30, type=int)
    data = AnalyticsService.get_category_breakdown(current_user.id, days)
    return jsonify(data)


@analytics_bp.route('/api/habit-progress', methods=['GET'])
@login_required
def get_habit_progress_api():
    """Get habit progress (API)"""
    data = AnalyticsService.get_habit_progress(current_user.id)
    return jsonify(data)


@analytics_bp.route('/api/dashboard', methods=['GET'])
@login_required
def get_dashboard_api():
    """Get complete dashboard data (API)"""
    data = AnalyticsService.get_dashboard_data(current_user.id)
    return jsonify(data)

