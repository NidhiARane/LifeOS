#!/usr/bin/env python
"""
Diagnostic script to capture exact error during report generation
"""
import os
import sys
import traceback

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.user import User
from app.services.ai_service import AIService

def capture_error():
    """Capture exact error during report generation"""
    app = create_app('development')

    with app.app_context():
        try:
            user = User.query.first()
            if not user:
                print("ERROR: No users found")
                return

            print(f"Generating report for user: {user.username}")
            print("-" * 80)

            # Test each component individually
            print("\n1. Testing financial insights...")
            try:
                financial = AIService.get_financial_insights(user.id)
                print(f"   OK: {financial}")
            except Exception as e:
                print(f"   ERROR: {type(e).__name__}: {str(e)}")
                traceback.print_exc()

            print("\n2. Testing health insights...")
            try:
                health = AIService.get_health_insights(user.id)
                print(f"   OK: {health}")
            except Exception as e:
                print(f"   ERROR: {type(e).__name__}: {str(e)}")
                traceback.print_exc()

            print("\n3. Testing habit analysis...")
            try:
                habits = AIService.analyze_habit_consistency(user.id)
                print(f"   OK: {habits}")
            except Exception as e:
                print(f"   ERROR: {type(e).__name__}: {str(e)}")
                traceback.print_exc()

            print("\n4. Testing full report generation...")
            try:
                report = AIService.generate_weekly_report(user.id)
                if 'error' in report:
                    print(f"   ERROR in report: {report['error']}")
                else:
                    print(f"   OK: Report generated")
                    print(f"   AI Summary length: {len(report.get('ai_summary', ''))}")
            except Exception as e:
                print(f"   ERROR: {type(e).__name__}: {str(e)}")
                traceback.print_exc()

            print("\n5. Testing Gemini API...")
            try:
                response = AIService.chat_with_gemini("Hello, test message", user.id)
                if response and 'error' not in response.lower():
                    print(f"   OK: Got response ({len(response)} chars)")
                else:
                    print(f"   ERROR: {response}")
            except Exception as e:
                print(f"   ERROR: {type(e).__name__}: {str(e)}")
                traceback.print_exc()

            print("\n" + "=" * 80)
            print("DIAGNOSTIC COMPLETE")
            print("=" * 80)

        except Exception as e:
            print(f"FATAL ERROR: {type(e).__name__}: {str(e)}")
            traceback.print_exc()

if __name__ == '__main__':
    capture_error()

