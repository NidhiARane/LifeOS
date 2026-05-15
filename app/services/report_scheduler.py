"""
Scheduled Task to Generate Weekly Reports Automatically
This module provides functionality to automatically generate weekly reports for all users
"""
from datetime import datetime, timedelta
from app import create_app, db
from app.models.user import User
from app.models.ai import AIReport
from app.services.ai_service import AIService
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WeeklyReportScheduler:
    """Scheduler for weekly report generation"""

    @staticmethod
    def generate_reports_for_all_users():
        """
        Generate weekly reports for all active users
        Should be called once per week (e.g., every Sunday)
        """
        app = create_app('development')

        with app.app_context():
            logger.info("=" * 80)
            logger.info("Starting Weekly Report Generation for All Users")
            logger.info("=" * 80)

            # Get all active users
            users = User.query.all()
            logger.info(f"Found {len(users)} users")

            success_count = 0
            error_count = 0

            for user in users:
                try:
                    logger.info(f"\nGenerating report for user: {user.username} (ID: {user.id})")

                    # Check if a report was already generated this week
                    week_ago = datetime.utcnow() - timedelta(days=7)
                    existing_report = AIReport.query.filter(
                        AIReport.user_id == user.id,
                        AIReport.report_date >= week_ago
                    ).first()

                    if existing_report:
                        logger.info(f"   Report already generated this week. Skipping.")
                        continue

                    # Generate the report
                    report_data = AIService.generate_weekly_report(user.id)

                    if 'error' in report_data:
                        logger.warning(f"   Error: {report_data['error']}")
                        error_count += 1
                        continue

                    # Safely serialize the data
                    try:
                        financial_summary = json.dumps(report_data.get('financial_summary', {}))
                    except (TypeError, ValueError):
                        financial_summary = json.dumps({})

                    try:
                        health_summary = json.dumps(report_data.get('health_summary', {}))
                    except (TypeError, ValueError):
                        health_summary = json.dumps({})

                    try:
                        habits_summary = json.dumps(report_data.get('habits_summary', {}))
                    except (TypeError, ValueError):
                        habits_summary = json.dumps({})

                    ai_summary = report_data.get('ai_summary', '')
                    if not ai_summary or len(ai_summary.strip()) == 0:
                        ai_summary = "Your weekly report is ready. Check back for AI-generated insights!"

                    # Create report record
                    report = AIReport(
                        user_id=user.id,
                        report_type='weekly',
                        title=f'Weekly Report - {datetime.utcnow().strftime("%B %d, %Y")}',
                        content=ai_summary,
                        financial_summary=financial_summary,
                        health_summary=health_summary,
                        habits_summary=habits_summary,
                        key_insights=ai_summary,
                        recommendations=ai_summary,
                        report_date=datetime.utcnow(),
                        week_start=datetime.fromisoformat(report_data['week_start']),
                        week_end=datetime.fromisoformat(report_data['week_end'])
                    )

                    db.session.add(report)
                    db.session.commit()

                    logger.info(f"   [SUCCESS] Report generated successfully!")
                    logger.info(f"   - AI Summary length: {len(ai_summary)} chars")
                    success_count += 1

                except Exception as e:
                    db.session.rollback()
                    logger.error(f"   [ERROR] Failed to generate report: {str(e)}")
                    import traceback
                    logger.error(traceback.format_exc())
                    error_count += 1

            logger.info("\n" + "=" * 80)
            logger.info(f"Weekly Report Generation Complete")
            logger.info(f"Success: {success_count}, Errors: {error_count}")
            logger.info("=" * 80)

            return {
                'total_users': len(users),
                'success': success_count,
                'errors': error_count
            }

    @staticmethod
    def generate_report_for_user(user_id):
        """
        Generate a weekly report for a specific user

        Args:
            user_id: The user's ID

        Returns:
            Dictionary with status information
        """
        app = create_app('development')

        with app.app_context():
            try:
                user = User.query.get(user_id)
                if not user:
                    return {'error': f'User with ID {user_id} not found'}

                # Generate the report
                report_data = AIService.generate_weekly_report(user_id)

                if 'error' in report_data:
                    return report_data

                # Safely serialize the data
                try:
                    financial_summary = json.dumps(report_data.get('financial_summary', {}))
                except (TypeError, ValueError):
                    financial_summary = json.dumps({})

                try:
                    health_summary = json.dumps(report_data.get('health_summary', {}))
                except (TypeError, ValueError):
                    health_summary = json.dumps({})

                try:
                    habits_summary = json.dumps(report_data.get('habits_summary', {}))
                except (TypeError, ValueError):
                    habits_summary = json.dumps({})

                ai_summary = report_data.get('ai_summary', '')

                # Create report record
                report = AIReport(
                    user_id=user_id,
                    report_type='weekly',
                    title=f'Weekly Report - {datetime.utcnow().strftime("%B %d, %Y")}',
                    content=ai_summary,
                    financial_summary=financial_summary,
                    health_summary=health_summary,
                    habits_summary=habits_summary,
                    key_insights=ai_summary,
                    recommendations=ai_summary,
                    report_date=datetime.utcnow(),
                    week_start=datetime.fromisoformat(report_data['week_start']),
                    week_end=datetime.fromisoformat(report_data['week_end'])
                )

                db.session.add(report)
                db.session.commit()

                return {
                    'status': 'success',
                    'report_id': report.id,
                    'title': report.title,
                    'message': 'Report generated successfully'
                }

            except Exception as e:
                db.session.rollback()
                import traceback
                logger.error(f"Error generating report for user {user_id}: {str(e)}")
                logger.error(traceback.format_exc())
                return {'error': str(e)}

def run_scheduled_task():
    """
    Entry point for running the scheduled task
    This can be called from a cron job or task scheduler
    """
    result = WeeklyReportScheduler.generate_reports_for_all_users()
    return result

if __name__ == '__main__':
    # Run the scheduler
    result = run_scheduled_task()
    print(f"Result: {result}")

