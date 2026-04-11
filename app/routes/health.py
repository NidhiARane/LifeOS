"""
Health Routes
Handles nutrition, meal logging, habits, and goals management
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from app.models.meal import Meal
from app.models.habit import Habit, HabitLog
from app.models.goal import Goal

health_bp = Blueprint('health', __name__, url_prefix='/health')


# ==================== MEAL ROUTES ====================

@health_bp.route('/meals', methods=['GET'])
@login_required
def meals_dashboard():
    """Display meals dashboard with logged meals"""
    page = request.args.get('page', 1, type=int)
    meals = Meal.query.filter_by(user_id=current_user.id).order_by(
        Meal.meal_date.desc()
    ).paginate(page=page, per_page=10)

    # Calculate daily totals for today
    today = datetime.utcnow().date()
    today_meals = Meal.query.filter_by(user_id=current_user.id).filter(
        db.func.date(Meal.meal_date) == today
    ).all()

    today_stats = {
        'calories': sum(m.calories for m in today_meals),
        'protein': sum(m.protein for m in today_meals),
        'carbs': sum(m.carbs for m in today_meals),
        'fat': sum(m.fat for m in today_meals)
    }

    return render_template('health/meals.html',
                          meals=meals,
                          today_stats=today_stats,
                          daily_calorie_goal=current_user.daily_calorie_goal,
                          daily_protein_goal=current_user.daily_protein_goal)


@health_bp.route('/meal/log', methods=['GET', 'POST'])
@login_required
def log_meal():
    """Log a new meal"""
    if request.method == 'POST':
        try:
            meal = Meal(
                user_id=current_user.id,
                name=request.form.get('meal_name'),
                description=request.form.get('description'),
                meal_type=request.form.get('meal_type'),
                calories=float(request.form.get('calories', 0)),
                protein=float(request.form.get('protein', 0)),
                carbs=float(request.form.get('carbs', 0)),
                fat=float(request.form.get('fat', 0)),
                meal_date=datetime.fromisoformat(request.form.get('meal_date', datetime.utcnow().isoformat()))
            )
            db.session.add(meal)
            db.session.commit()
            flash(f'Meal "{meal.name}" logged successfully!', 'success')
            return redirect(url_for('health.meals_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error logging meal: {str(e)}', 'danger')

    return render_template('health/log_meal.html', now=datetime.utcnow())


@health_bp.route('/meal/<int:meal_id>/delete', methods=['POST'])
@login_required
def delete_meal(meal_id):
    """Delete a meal"""
    meal = Meal.query.get_or_404(meal_id)
    if meal.user_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('health.meals_dashboard'))

    meal_name = meal.name
    db.session.delete(meal)
    db.session.commit()
    flash(f'Meal "{meal_name}" deleted successfully!', 'success')
    return redirect(url_for('health.meals_dashboard'))


# ==================== HABIT ROUTES ====================

@health_bp.route('/habits', methods=['GET'])
@login_required
def habits_dashboard():
    """Display habits dashboard"""
    habits = Habit.query.filter_by(user_id=current_user.id).all()

    # Calculate consistency scores
    habit_stats = []
    for habit in habits:
        total_logs = len(habit.logs)
        days_since_created = (datetime.utcnow() - habit.created_at).days + 1

        consistency_score = 0
        if days_since_created > 0:
            consistency_score = (total_logs / days_since_created) * 100

        habit_stats.append({
            'habit': habit,
            'total_logs': total_logs,
            'consistency_score': round(consistency_score, 2),
            'days_since_created': days_since_created
        })

    return render_template('health/habits.html', habit_stats=habit_stats)


@health_bp.route('/habit/create', methods=['GET', 'POST'])
@login_required
def create_habit():
    """Create a new habit"""
    if request.method == 'POST':
        try:
            habit = Habit(
                user_id=current_user.id,
                name=request.form.get('habit_name'),
                description=request.form.get('description'),
                category=request.form.get('category'),
                frequency=request.form.get('frequency'),
                target=int(request.form.get('target', 1)),
                is_active=True
            )
            db.session.add(habit)
            db.session.commit()
            flash(f'Habit "{habit.name}" created successfully!', 'success')
            return redirect(url_for('health.habits_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating habit: {str(e)}', 'danger')

    return render_template('health/create_habit.html')


@health_bp.route('/habit/<int:habit_id>/checkin', methods=['POST'])
@login_required
def checkin_habit(habit_id):
    """Check in a habit"""
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        # Check if already checked in today
        today = datetime.utcnow().date()
        existing_log = HabitLog.query.filter_by(habit_id=habit_id).filter(
            db.func.date(HabitLog.completed_date) == today
        ).first()

        if existing_log:
            return jsonify({'error': 'Already checked in today'}), 400

        # Create new log
        log = HabitLog(habit_id=habit_id)
        db.session.add(log)

        # Update streaks
        yesterday = today - timedelta(days=1)
        last_log = HabitLog.query.filter_by(habit_id=habit_id).filter(
            db.func.date(HabitLog.completed_date) == yesterday
        ).first()

        if last_log:
            habit.current_streak += 1
        else:
            habit.current_streak = 1

        if habit.current_streak > habit.longest_streak:
            habit.longest_streak = habit.current_streak

        db.session.commit()
        return jsonify({
            'status': 'success',
            'current_streak': habit.current_streak,
            'longest_streak': habit.longest_streak
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@health_bp.route('/habit/<int:habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    """Delete a habit"""
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('health.habits_dashboard'))

    habit_name = habit.name
    db.session.delete(habit)
    db.session.commit()
    flash(f'Habit "{habit_name}" deleted successfully!', 'success')
    return redirect(url_for('health.habits_dashboard'))


# ==================== GOAL ROUTES ====================

@health_bp.route('/goals', methods=['GET'])
@login_required
def goals_dashboard():
    """Display goals dashboard"""
    goals = Goal.query.filter_by(user_id=current_user.id).all()

    # Categorize goals
    categorized_goals = {}
    for goal in goals:
        category = goal.category or 'Other'
        if category not in categorized_goals:
            categorized_goals[category] = []
        categorized_goals[category].append(goal)

    return render_template('health/goals.html', categorized_goals=categorized_goals, goals=goals)


@health_bp.route('/goal/create', methods=['GET', 'POST'])
@login_required
def create_goal():
    """Create a new goal"""
    if request.method == 'POST':
        try:
            target_date = request.form.get('target_date')
            goal = Goal(
                user_id=current_user.id,
                title=request.form.get('goal_title'),
                description=request.form.get('description'),
                category=request.form.get('category'),
                target_value=float(request.form.get('target_value')),
                unit=request.form.get('unit'),
                priority=request.form.get('priority', 'medium'),
                target_date=datetime.fromisoformat(target_date) if target_date else None
            )
            db.session.add(goal)
            db.session.commit()
            flash(f'Goal "{goal.title}" created successfully!', 'success')
            return redirect(url_for('health.goals_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating goal: {str(e)}', 'danger')

    return render_template('health/create_goal.html')


@health_bp.route('/goal/<int:goal_id>/update-progress', methods=['POST'])
@login_required
def update_goal_progress(goal_id):
    """Update goal progress"""
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        data = request.get_json()
        current_value = float(data.get('current_value', 0))
        goal.current_value = current_value

        # Calculate progress percentage
        if goal.target_value > 0:
            progress = (current_value / goal.target_value) * 100
            goal.is_completed = progress >= 100

        db.session.commit()
        return jsonify({
            'status': 'success',
            'current_value': goal.current_value,
            'progress': goal.get_progress_percentage()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@health_bp.route('/goal/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete_goal(goal_id):
    """Delete a goal"""
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('health.goals_dashboard'))

    goal_title = goal.title
    db.session.delete(goal)
    db.session.commit()
    flash(f'Goal "{goal_title}" deleted successfully!', 'success')
    return redirect(url_for('health.goals_dashboard'))


# ==================== API ROUTES ====================

@health_bp.route('/api/meals-summary', methods=['GET'])
@login_required
def get_meals_summary():
    """Get meals summary for the last 7 days (API)"""
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    meals = Meal.query.filter_by(user_id=current_user.id).filter(
        Meal.meal_date >= seven_days_ago
    ).all()

    daily_summary = {}
    for meal in meals:
        date = meal.meal_date.date().isoformat()
        if date not in daily_summary:
            daily_summary[date] = {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'meals': []
            }

        daily_summary[date]['calories'] += meal.calories
        daily_summary[date]['protein'] += meal.protein
        daily_summary[date]['carbs'] += meal.carbs
        daily_summary[date]['fat'] += meal.fat
        daily_summary[date]['meals'].append(meal.to_dict())

    return jsonify(daily_summary)


@health_bp.route('/api/habits-summary', methods=['GET'])
@login_required
def get_habits_summary():
    """Get habits summary (API)"""
    habits = Habit.query.filter_by(user_id=current_user.id).all()

    summary = {
        'total_habits': len(habits),
        'active_habits': len([h for h in habits if h.is_active]),
        'habits': [h.to_dict() for h in habits]
    }

    return jsonify(summary)


@health_bp.route('/api/goals-summary', methods=['GET'])
@login_required
def get_goals_summary():
    """Get goals summary (API)"""
    goals = Goal.query.filter_by(user_id=current_user.id).all()

    summary = {
        'total_goals': len(goals),
        'completed_goals': len([g for g in goals if g.is_completed]),
        'goals': [g.to_dict() for g in goals]
    }

    return jsonify(summary)

