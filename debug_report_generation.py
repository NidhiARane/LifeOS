#!/usr/bin/env python
"""
Debug script to test weekly report generation
"""
import os
import sys
from dotenv import load_dotenv

# Fix encoding for Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from app import create_app, db
from app.models.user import User
from app.models.expense import Expense
from app.models.meal import Meal
from app.models.habit import Habit, HabitLog
from app.services.ai_service import AIService
from datetime import datetime, timedelta

def test_report_generation():
    """Test weekly report generation"""
    app = create_app('development')

    with app.app_context():
        print("=" * 80)
        print("WEEKLY REPORT GENERATION DEBUG")
        print("=" * 80)

        # Get first user
        user = User.query.first()
        if not user:
            print("[ERROR] No users found in database")
            return

        print(f"\n[TEST] Testing with user: {user.username} (ID: {user.id})")

        # Check if user has data
        expenses = Expense.query.filter_by(user_id=user.id).count()
        meals = Meal.query.filter_by(user_id=user.id).count()
        habits = Habit.query.filter_by(user_id=user.id).count()

        print(f"\n[DATA] User Data Status:")
        print(f"   - Expenses: {expenses}")
        print(f"   - Meals: {meals}")
        print(f"   - Habits: {habits}")

        if expenses == 0 and meals == 0 and habits == 0:
            print("\n[WARNING] User has no data. Cannot generate meaningful report.")
            print("   Please log some expenses, meals, and create habits first.")
            return

        # Test financial insights
        print(f"\n[TEST] Testing Financial Insights:")
        try:
            financial = AIService.get_financial_insights(user.id)
            if 'error' in financial:
                print(f"   [ERROR] {financial['error']}")
            else:
                print(f"   [OK] Total spent: ${financial.get('total_spent', 0)}")
                print(f"   [OK] Average daily: ${financial.get('average_daily', 0)}")
                print(f"   [OK] Top categories: {len(financial.get('top_categories', []))} found")
        except Exception as e:
            print(f"   [ERROR] Exception: {str(e)}")

        # Test health insights
        print(f"\n[TEST] Testing Health Insights:")
        try:
            health = AIService.get_health_insights(user.id)
            if 'error' in health:
                print(f"   [ERROR] {health['error']}")
            else:
                print(f"   [OK] Avg calories: {health.get('avg_daily_calories', 0)}")
                print(f"   [OK] Avg protein: {health.get('avg_daily_protein', 0)}g")
                print(f"   [OK] Active habits: {health.get('active_habits', 0)}")
        except Exception as e:
            print(f"   [ERROR] Exception: {str(e)}")

        # Test habit analysis
        print(f"\n[TEST] Testing Habit Analysis:")
        try:
            habits_analysis = AIService.analyze_habit_consistency(user.id)
            if 'error' in habits_analysis:
                print(f"   [ERROR] {habits_analysis['error']}")
            else:
                print(f"   [OK] Total habits: {habits_analysis.get('total_habits', 0)}")
                print(f"   [OK] Average completion: {habits_analysis.get('average_completion', 0)}%")
        except Exception as e:
            print(f"   [ERROR] Exception: {str(e)}")

        # Test expense prediction
        print(f"\n[TEST] Testing Expense Prediction:")
        try:
            prediction = AIService.predict_expenses(user.id)
            if 'error' in prediction:
                print(f"   [NOTE] {prediction['error']}")
            else:
                print(f"   [OK] Predicted daily: ${prediction.get('predicted_daily_expense', 0)}")
                print(f"   [OK] Confidence: {prediction.get('confidence', 'Unknown')}")
        except Exception as e:
            print(f"   [ERROR] Exception: {str(e)}")

        # Test Gemini API
        print(f"\n[TEST] Testing Gemini API:")
        try:
            if not app.config.get('GEMINI_API_KEY'):
                print(f"   [ERROR] GEMINI_API_KEY not configured")
            else:
                print(f"   [OK] GEMINI_API_KEY is set")

                # Test simple message
                response = AIService.chat_with_gemini(
                    "Hello, introduce yourself as LifeOS AI Assistant",
                    user.id
                )

                if response and 'error' not in response.lower():
                    print(f"   [OK] API response received ({len(response)} chars)")
                    print(f"   Sample: {response[:100]}...")
                else:
                    print(f"   [ERROR] API Error: {response}")
        except Exception as e:
            print(f"   [ERROR] Exception: {str(e)}")

        # Test full report generation
        print(f"\n[TEST] Testing Full Report Generation:")
        try:
            report = AIService.generate_weekly_report(user.id)

            if 'error' in report:
                print(f"   [ERROR] {report['error']}")
            else:
                print(f"   [OK] Report generated successfully!")
                print(f"   [OK] AI Summary length: {len(report.get('ai_summary', ''))} chars")
                print(f"   [OK] Week: {report.get('week_start')} to {report.get('week_end')}")
                print(f"\n   [CONTENT] Sample AI Summary:")
                print(f"   {report.get('ai_summary', '')[:200]}...")
        except Exception as e:
            print(f"   [ERROR] Exception: {str(e)}")
            import traceback
            traceback.print_exc()

        print("\n" + "=" * 80)
        print("DEBUG TEST COMPLETE")
        print("=" * 80)

if __name__ == '__main__':
    test_report_generation()

