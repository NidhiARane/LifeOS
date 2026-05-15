#!/usr/bin/env python
"""
Simple debug script to test weekly report generation
Writes output to file instead of console to avoid encoding issues
"""
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from app import create_app, db
from app.models.user import User
from app.models.expense import Expense
from app.models.meal import Meal
from app.models.habit import Habit
from app.services.ai_service import AIService

def test_report_generation():
    app = create_app('development')

    output = []
    output.append("=" * 80)
    output.append("WEEKLY REPORT GENERATION DEBUG")
    output.append("=" * 80)

    with app.app_context():
        try:
            user = User.query.first()
            if not user:
                output.append("\n[ERROR] No users found in database")
                with open('debug_report.log', 'w') as f:
                    f.write('\n'.join(output))
                return

            output.append(f"\n[TEST] Testing with user: {user.username} (ID: {user.id})")

            expenses = Expense.query.filter_by(user_id=user.id).count()
            meals = Meal.query.filter_by(user_id=user.id).count()
            habits = Habit.query.filter_by(user_id=user.id).count()

            output.append(f"\n[DATA] User Data Status:")
            output.append(f"   - Expenses: {expenses}")
            output.append(f"   - Meals: {meals}")
            output.append(f"   - Habits: {habits}")

            if expenses == 0 and meals == 0 and habits == 0:
                output.append("\n[WARNING] User has no data. Cannot generate meaningful report.")
                with open('debug_report.log', 'w') as f:
                    f.write('\n'.join(output))
                return

            output.append(f"\n[TEST] Testing Financial Insights:")
            try:
                financial = AIService.get_financial_insights(user.id)
                if 'error' in financial:
                    output.append(f"   [ERROR] {financial['error']}")
                else:
                    output.append(f"   [OK] Total spent: ${financial.get('total_spent', 0)}")
                    output.append(f"   [OK] Average daily: ${financial.get('average_daily', 0)}")
            except Exception as e:
                output.append(f"   [ERROR] {str(e)}")

            output.append(f"\n[TEST] Testing Health Insights:")
            try:
                health = AIService.get_health_insights(user.id)
                if 'error' in health:
                    output.append(f"   [ERROR] {health['error']}")
                else:
                    output.append(f"   [OK] Avg calories: {health.get('avg_daily_calories', 0)}")
            except Exception as e:
                output.append(f"   [ERROR] {str(e)}")

            output.append(f"\n[TEST] Testing Full Report Generation:")
            try:
                report = AIService.generate_weekly_report(user.id)

                if 'error' in report:
                    output.append(f"   [ERROR] {report['error']}")
                else:
                    output.append(f"   [SUCCESS] Report generated!")
                    output.append(f"   [OK] AI Summary length: {len(report.get('ai_summary', ''))}")
                    output.append(f"   [OK] Week start: {report.get('week_start')}")
                    summary_preview = str(report.get('ai_summary', ''))[:150]
                    output.append(f"   [PREVIEW] {summary_preview}")
            except Exception as e:
                output.append(f"   [ERROR] {str(e)}")
                import traceback
                output.append(traceback.format_exc())

        except Exception as e:
            output.append(f"[FATAL ERROR] {str(e)}")
            import traceback
            output.append(traceback.format_exc())

    output.append("\n" + "=" * 80)
    output.append("DEBUG TEST COMPLETE")
    output.append("=" * 80)

    # Write to file
    with open('debug_report.log', 'w') as f:
        f.write('\n'.join(output))

    # Print summary
    print("Debug output written to debug_report.log")
    for line in output[-10:]:
        print(line)

if __name__ == '__main__':
    test_report_generation()

