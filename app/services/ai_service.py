"""
AI Service
Handles AI-powered features including Gemini chat, insights, and ML predictions
"""
import google.generativeai as genai
from flask import current_app
from datetime import datetime, timedelta
import json
from app import db
from app.models.meal import Meal
from app.models.habit import Habit, HabitLog
from app.models.expense import Expense
from app.models.goal import Goal
from sklearn.linear_model import LinearRegression
import numpy as np

class AIService:
    """AI Service for Gemini integration and ML predictions"""

    @staticmethod
    def initialize_gemini():
        """Initialize Gemini API"""
        api_key = current_app.config.get('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            return True
        return False

    @staticmethod
    def chat_with_gemini(user_message, user_id, context_data=None):
        """
        Send a message to Gemini and get a response

        Args:
            user_message: The user's message
            user_id: The user's ID for context
            context_data: Optional context data (meals, habits, expenses, etc.)

        Returns:
            AI response text
        """
        try:
            if not AIService.initialize_gemini():
                return "AI Assistant is not configured. Please set GEMINI_API_KEY in environment."

            model = genai.GenerativeModel('gemini-2.5-flash-lite')

            # Build context
            context_prompt = ""
            if context_data:
                if 'meals' in context_data:
                    context_prompt += f"\nUser's recent meals: {context_data['meals']}"
                if 'habits' in context_data:
                    context_prompt += f"\nUser's habits: {context_data['habits']}"
                if 'expenses' in context_data:
                    context_prompt += f"\nUser's spending: {context_data['expenses']}"
                if 'goals' in context_data:
                    context_prompt += f"\nUser's goals: {context_data['goals']}"

            # Create prompt
            full_prompt = f"""You are LifeOS AI Assistant, a helpful personal life management advisor.
            
{context_prompt}

User Message: {user_message}

Provide helpful, personalized advice based on the user's data. Be concise but helpful."""

            response = model.generate_content(full_prompt)
            return response.text

        except Exception as e:
            return f"Error communicating with AI: {str(e)}"

    @staticmethod
    def get_financial_insights(user_id):
        """
        Generate financial insights from expense data

        Args:
            user_id: The user's ID

        Returns:
            Dictionary with financial insights
        """
        try:
            # Get last 30 days of expenses
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            expenses = Expense.query.filter_by(user_id=user_id).filter(
                Expense.expense_date >= thirty_days_ago
            ).all()

            if not expenses:
                return {
                    'total_spent': 0,
                    'average_daily': 0,
                    'top_categories': [],
                    'trend': 'No data'
                }

            # Calculate metrics
            total_spent = sum(e.amount for e in expenses)
            avg_daily = total_spent / 30

            # Group by category
            categories = {}
            for expense in expenses:
                cat = expense.category.name if expense.category else 'Other'
                categories[cat] = categories.get(cat, 0) + expense.amount

            top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]

            return {
                'total_spent': round(total_spent, 2),
                'average_daily': round(avg_daily, 2),
                'top_categories': [{'name': cat, 'amount': amount} for cat, amount in top_categories],
                'expense_count': len(expenses),
                'trend': 'Increasing' if avg_daily > 50 else 'Moderate'
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_health_insights(user_id):
        """
        Generate health insights from meal and habit data

        Args:
            user_id: The user's ID

        Returns:
            Dictionary with health insights
        """
        try:
            # Get last 7 days of meals
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            meals = Meal.query.filter_by(user_id=user_id).filter(
                Meal.meal_date >= seven_days_ago
            ).all()

            # Get habits
            habits = Habit.query.filter_by(user_id=user_id).all()

            # Calculate meal metrics
            avg_calories = sum(m.calories for m in meals) / len(meals) if meals else 0
            avg_protein = sum(m.protein for m in meals) / len(meals) if meals else 0

            # Calculate habit consistency based on last 30 days
            avg_consistency = 0
            if habits:
                thirty_days_ago = datetime.utcnow() - timedelta(days=30)
                for habit in habits:
                    # Count logs in the last 30 days (not since habit creation)
                    recent_logs = [log for log in habit.logs if log.completed_date >= thirty_days_ago]
                    # Max 1 log per day, so max completion is 100% over 30 days
                    consistency = (len(recent_logs) / 30 * 100) if recent_logs else 0
                    consistency = min(100, consistency)  # Cap at 100%
                    avg_consistency += consistency
                avg_consistency = avg_consistency / len(habits)

            return {
                'avg_daily_calories': round(avg_calories, 0),
                'avg_daily_protein': round(avg_protein, 1),
                'meals_logged': len(meals),
                'active_habits': len([h for h in habits if h.is_active]),
                'habit_consistency': round(min(100, avg_consistency), 1),
                'health_status': 'Good' if avg_consistency > 70 else 'Fair' if avg_consistency > 40 else 'Needs Improvement'
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def predict_expenses(user_id, days_ahead=30):
        """
        Predict future expenses using linear regression

        Args:
            user_id: The user's ID
            days_ahead: Number of days to predict ahead

        Returns:
            Predicted daily expense amount
        """
        try:
            # Get last 90 days of expenses
            ninety_days_ago = datetime.utcnow() - timedelta(days=90)
            expenses = Expense.query.filter_by(user_id=user_id).filter(
                Expense.expense_date >= ninety_days_ago
            ).all()

            if len(expenses) < 10:
                return {'error': 'Not enough data for prediction', 'days_of_data': len(expenses)}

            # Group by day
            daily_expenses = {}
            for expense in expenses:
                date = expense.expense_date.date()
                daily_expenses[date] = daily_expenses.get(date, 0) + expense.amount

            # Prepare data for model
            X = np.array(range(len(daily_expenses))).reshape(-1, 1)
            y = np.array(list(daily_expenses.values()))

            # Train model
            model = LinearRegression()
            model.fit(X, y)

            # Predict
            future_day = len(daily_expenses) + days_ahead
            predicted_expense = model.predict([[future_day]])[0]

            return {
                'predicted_daily_expense': round(max(0, predicted_expense), 2),
                'based_on_days': len(daily_expenses),
                'confidence': 'Moderate' if len(daily_expenses) > 30 else 'Low'
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def predict_weight_trend(user_id, days_ahead=30):
        """
        Predict weight trend using linear regression
        (Requires weight data to be tracked - placeholder implementation)

        Args:
            user_id: The user's ID
            days_ahead: Number of days to predict ahead

        Returns:
            Weight trend prediction
        """
        try:
            # This would require weight tracking in the system
            # For now, return a placeholder response
            return {
                'trend': 'Data not available',
                'note': 'Weight tracking feature not yet implemented',
                'recommendation': 'Start logging your weight regularly for predictions'
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def analyze_habit_consistency(user_id):
        """
        Analyze habit consistency patterns

        Args:
            user_id: The user's ID

        Returns:
            Habit consistency analysis
        """
        try:
            habits = Habit.query.filter_by(user_id=user_id).all()

            if not habits:
                return {'total_habits': 0, 'habits': []}

            habit_analysis = []
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            for habit in habits:
                # Count logs in the last 30 days (not since habit creation)
                recent_logs = [log for log in habit.logs if log.completed_date >= thirty_days_ago]
                # Max 1 log per day, so max completion is 100% over 30 days
                completion_rate = (len(recent_logs) / 30 * 100) if recent_logs else 0
                completion_rate = min(100, completion_rate)  # Cap at 100%

                habit_analysis.append({
                    'name': habit.name,
                    'current_streak': habit.current_streak,
                    'longest_streak': habit.longest_streak,
                    'completion_rate': round(completion_rate, 1),
                    'status': 'Excellent' if completion_rate > 80 else 'Good' if completion_rate > 60 else 'Fair' if completion_rate > 40 else 'Needs Work',
                    'days_active': (datetime.utcnow() - habit.created_at).days + 1
                })

            return {
                'total_habits': len(habits),
                'habits': habit_analysis,
                'average_completion': round(min(100, sum(h['completion_rate'] for h in habit_analysis) / len(habit_analysis)), 1)
            }

        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def generate_weekly_report(user_id):
        """
        Generate comprehensive weekly AI report

        Args:
            user_id: The user's ID

        Returns:
            Weekly report data
        """
        try:
            # Get all insights
            financial = AIService.get_financial_insights(user_id)
            health = AIService.get_health_insights(user_id)
            habits = AIService.analyze_habit_consistency(user_id)
            expense_prediction = AIService.predict_expenses(user_id, days_ahead=7)

            # Check for errors in any of the data collections
            if 'error' in financial or 'error' in health or 'error' in habits:
                return {'error': 'Failed to gather user data for report generation'}

            # Generate summary with AI
            # Format the data more carefully for the prompt
            categories_str = ', '.join([f"{cat['name']}: ${cat['amount']:.2f}" for cat in financial.get('top_categories', [])])
            if not categories_str:
                categories_str = "No expense data available"

            summary_prompt = f"""Based on the following weekly life management data, provide a brief personalized summary (2-3 paragraphs) and 3 key recommendations:

Financial Summary:
- Total spent: ${financial.get('total_spent', 0)}
- Average daily: ${financial.get('average_daily', 0)}
- Top spending categories: {categories_str}
- Spending trend: {financial.get('trend', 'Unknown')}

Health Summary:
- Average daily calories: {health.get('avg_daily_calories', 0)}
- Average daily protein: {health.get('avg_daily_protein', 0)}g
- Active habits: {health.get('active_habits', 0)}
- Habit consistency: {health.get('habit_consistency', 0)}%
- Overall health status: {health.get('health_status', 'Unknown')}

Habit Analysis:
- Total habits tracked: {habits.get('total_habits', 0)}
- Average completion rate: {habits.get('average_completion', 0)}%

Please provide:
1. A summary of the user's week
2. Areas of strength to build on
3. Three specific, actionable recommendations for improvement

Be encouraging and supportive in your tone."""

            ai_summary = AIService.chat_with_gemini(summary_prompt, user_id)

            # Handle case where AI response contains error
            if isinstance(ai_summary, str) and 'error' in ai_summary.lower():
                # Fallback to a template response
                ai_summary = f"""Weekly Summary: Based on your data, you spent ${financial.get('total_spent', 0)} over 7 days with an average of ${financial.get('average_daily', 0)} per day. You logged {health.get('avg_daily_calories', 0)} calories on average and maintained {health.get('habit_consistency', 0)}% habit consistency. Keep up the good work and consider the recommendations for improvement!"""

            report = {
                'week_start': (datetime.utcnow() - timedelta(days=7)).isoformat(),
                'week_end': datetime.utcnow().isoformat(),
                'financial_summary': financial,
                'health_summary': health,
                'habits_summary': habits,
                'ai_summary': ai_summary,
                'expense_prediction': expense_prediction,
                'generated_at': datetime.utcnow().isoformat()
            }

            return report

        except Exception as e:
            import traceback
            print(f"Error generating weekly report: {str(e)}")
            traceback.print_exc()
            return {'error': str(e)}

