"""
Analytics Service
Handles analytics calculations, Life Score generation, and dashboard data
"""
from datetime import datetime, timedelta
from app import db
from app.models.analytics import LifeScore, UserBudget
from app.models.expense import Expense
from app.models.meal import Meal
from app.models.habit import Habit
from app.models.goal import Goal
import json


class AnalyticsService:
    """Service for calculating analytics and Life Score"""

    @staticmethod
    def get_or_create_budget(user_id, monthly_limit=3000):
        """Get or create user budget"""
        budget = UserBudget.query.filter_by(user_id=user_id).first()
        if not budget:
            budget = UserBudget(user_id=user_id, monthly_limit=monthly_limit)
            db.session.add(budget)
            db.session.commit()
        return budget

    @staticmethod
    def calculate_health_score(user_id):
        """
        Calculate health discipline score based on:
        - Calorie logging consistency
        - Meal frequency
        - Habit adherence to health habits

        Returns: Score 0-100
        """
        try:
            # Get last 30 days of meals
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            meals = Meal.query.filter_by(user_id=user_id).filter(
                Meal.meal_date >= thirty_days_ago
            ).all()

            # Get habits (filter health-related if tagged)
            habits = Habit.query.filter_by(user_id=user_id).all()

            # Meal logging score (50%)
            meal_score = 0
            if meals:
                # More meals logged = better score (max 100 meals in 30 days)
                meal_score = min(100, (len(meals) / 100) * 100)

            # Habit consistency score (50%)
            habit_score = 0
            if habits:
                total_completion = 0
                for habit in habits:
                    days_active = (datetime.utcnow() - habit.created_at).days + 1
                    completion = (len(habit.logs) / days_active * 100) if days_active > 0 else 0
                    total_completion += completion
                habit_score = total_completion / len(habits)

            # Combined health score
            health_score = (meal_score * 0.5) + (habit_score * 0.5)
            return round(min(100, health_score), 1)

        except Exception as e:
            return 0

    @staticmethod
    def calculate_financial_score(user_id):
        """
        Calculate financial discipline score based on:
        - Budget adherence
        - Expense tracking consistency
        - Spending trend

        Returns: Score 0-100
        """
        try:
            budget = AnalyticsService.get_or_create_budget(user_id)

            # Get last 30 days of expenses
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            expenses = Expense.query.filter_by(user_id=user_id).filter(
                Expense.expense_date >= thirty_days_ago
            ).all()

            if not expenses:
                return 50  # Default score if no data

            total_spent = sum(e.amount for e in expenses)
            budget_limit = budget.monthly_limit

            # Budget adherence score (60%)
            if total_spent <= budget_limit:
                budget_score = 100
            else:
                # Reduce score based on overspending
                overage_percent = ((total_spent - budget_limit) / budget_limit) * 100
                budget_score = max(0, 100 - overage_percent)

            # Expense tracking score (40%) - more consistent tracking = higher score
            expense_score = min(100, (len(expenses) / 30) * 100)  # Track ~1 expense per day

            # Combined financial score
            financial_score = (budget_score * 0.6) + (expense_score * 0.4)
            return round(min(100, financial_score), 1)

        except Exception as e:
            return 0

    @staticmethod
    def calculate_habit_score(user_id):
        """
        Calculate habit consistency score based on:
        - Overall completion rates
        - Current streaks
        - Days active

        Returns: Score 0-100
        """
        try:
            habits = Habit.query.filter_by(user_id=user_id).all()

            if not habits:
                return 50  # Default score if no habits

            total_completion = 0
            for habit in habits:
                days_active = (datetime.utcnow() - habit.created_at).days + 1
                completion_rate = (len(habit.logs) / days_active * 100) if days_active > 0 else 0
                total_completion += completion_rate

            habit_score = total_completion / len(habits)
            return round(min(100, habit_score), 1)

        except Exception as e:
            return 0

    @staticmethod
    def calculate_life_score(user_id):
        """
        Calculate overall Life Score based on:
        - Health Discipline (33%)
        - Financial Discipline (33%)
        - Habit Consistency (34%)

        Returns: Life Score 0-100
        """
        try:
            # Calculate component scores
            health_score = AnalyticsService.calculate_health_score(user_id)
            financial_score = AnalyticsService.calculate_financial_score(user_id)
            habit_score = AnalyticsService.calculate_habit_score(user_id)

            # Calculate overall score with equal weights
            overall_score = (health_score + financial_score + habit_score) / 3

            # Save to database
            life_score = LifeScore.query.filter_by(user_id=user_id).first()
            if not life_score:
                life_score = LifeScore(user_id=user_id)

            life_score.overall_score = round(overall_score, 1)
            life_score.health_score = health_score
            life_score.financial_score = financial_score
            life_score.habit_score = habit_score
            life_score.health_discipline = health_score
            life_score.financial_discipline = financial_score
            life_score.habit_consistency = habit_score
            life_score.calculated_at = datetime.utcnow()

            db.session.add(life_score)
            db.session.commit()

            return life_score.to_dict()

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_expense_summary(user_id, days=30):
        """Get expense summary for last N days"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            expenses = Expense.query.filter_by(user_id=user_id).filter(
                Expense.expense_date >= start_date
            ).all()

            budget = AnalyticsService.get_or_create_budget(user_id)
            total_spent = sum(e.amount for e in expenses)
            remaining = budget.monthly_limit - total_spent
            percentage = (total_spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0

            # Category breakdown
            categories = {}
            for expense in expenses:
                cat_name = expense.category.name if expense.category else 'Other'
                if cat_name not in categories:
                    categories[cat_name] = 0
                categories[cat_name] += expense.amount

            return {
                'total_spent': round(total_spent, 2),
                'budget_limit': budget.monthly_limit,
                'remaining': round(max(0, remaining), 2),
                'percentage': round(percentage, 1),
                'expense_count': len(expenses),
                'categories': categories,
                'status': 'Within Budget' if total_spent <= budget.monthly_limit else 'Over Budget'
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_health_summary(user_id, days=30):
        """Get health summary for last N days"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            meals = Meal.query.filter_by(user_id=user_id).filter(
                Meal.meal_date >= start_date
            ).all()

            if not meals:
                return {
                    'avg_calories': 0,
                    'avg_protein': 0,
                    'total_meals': 0,
                    'calories_per_meal': 0
                }

            total_calories = sum(m.calories for m in meals)
            total_protein = sum(m.protein for m in meals)
            avg_calories = total_calories / len(meals)
            avg_protein = total_protein / len(meals)

            return {
                'avg_calories': round(avg_calories, 1),
                'avg_protein': round(avg_protein, 1),
                'total_meals': len(meals),
                'calories_per_meal': round(total_calories / len(meals) if meals else 0, 1),
                'total_calories': round(total_calories, 0),
                'total_protein': round(total_protein, 1)
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_daily_expenses(user_id, days=30):
        """Get daily expense data for charts"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            expenses = Expense.query.filter_by(user_id=user_id).filter(
                Expense.expense_date >= start_date
            ).order_by(Expense.expense_date).all()

            # Group by date
            daily_data = {}
            for expense in expenses:
                date = expense.expense_date.date().isoformat()
                if date not in daily_data:
                    daily_data[date] = 0
                daily_data[date] += expense.amount

            return {
                'dates': sorted(daily_data.keys()),
                'amounts': [daily_data[date] for date in sorted(daily_data.keys())],
                'data': daily_data
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_daily_calories(user_id, days=30):
        """Get daily calorie data for charts"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            meals = Meal.query.filter_by(user_id=user_id).filter(
                Meal.meal_date >= start_date
            ).order_by(Meal.meal_date).all()

            # Group by date
            daily_data = {}
            for meal in meals:
                date = meal.meal_date.date().isoformat()
                if date not in daily_data:
                    daily_data[date] = {'calories': 0, 'protein': 0}
                daily_data[date]['calories'] += meal.calories
                daily_data[date]['protein'] += meal.protein

            return {
                'dates': sorted(daily_data.keys()),
                'calories': [daily_data[date]['calories'] for date in sorted(daily_data.keys())],
                'protein': [daily_data[date]['protein'] for date in sorted(daily_data.keys())],
                'data': daily_data
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_category_breakdown(user_id, days=30):
        """Get expense category breakdown"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            expenses = Expense.query.filter_by(user_id=user_id).filter(
                Expense.expense_date >= start_date
            ).all()

            categories = {}
            for expense in expenses:
                cat_name = expense.category.name if expense.category else 'Other'
                if cat_name not in categories:
                    categories[cat_name] = 0
                categories[cat_name] += expense.amount

            # Sort by amount
            sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

            return {
                'labels': [cat[0] for cat in sorted_categories],
                'data': [round(cat[1], 2) for cat in sorted_categories],
                'total': round(sum(categories.values()), 2)
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_habit_progress(user_id, days=30):
        """Get habit completion progress"""
        try:
            habits = Habit.query.filter_by(user_id=user_id).all()

            if not habits:
                return {'habits': [], 'average_completion': 0}

            habit_data = []
            total_completion = 0

            for habit in habits:
                days_active = (datetime.utcnow() - habit.created_at).days + 1
                completion_rate = (len(habit.logs) / days_active * 100) if days_active > 0 else 0

                habit_data.append({
                    'name': habit.name,
                    'completion_rate': round(completion_rate, 1),
                    'current_streak': habit.current_streak,
                    'longest_streak': habit.longest_streak,
                    'days_active': days_active
                })

                total_completion += completion_rate

            avg_completion = (total_completion / len(habits)) if habits else 0

            return {
                'habits': habit_data,
                'average_completion': round(avg_completion, 1),
                'total_habits': len(habits)
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_dashboard_data(user_id):
        """Get complete dashboard data"""
        try:
            # Calculate Life Score
            life_score_data = AnalyticsService.calculate_life_score(user_id)

            # Get summaries
            expense_summary = AnalyticsService.get_expense_summary(user_id)
            health_summary = AnalyticsService.get_health_summary(user_id)
            habit_progress = AnalyticsService.get_habit_progress(user_id)

            # Get chart data
            daily_expenses = AnalyticsService.get_daily_expenses(user_id)
            daily_calories = AnalyticsService.get_daily_calories(user_id)
            category_breakdown = AnalyticsService.get_category_breakdown(user_id)

            return {
                'life_score': life_score_data,
                'expense_summary': expense_summary,
                'health_summary': health_summary,
                'habit_progress': habit_progress,
                'daily_expenses': daily_expenses,
                'daily_calories': daily_calories,
                'category_breakdown': category_breakdown
            }

        except Exception as e:
            return {'error': str(e)}

