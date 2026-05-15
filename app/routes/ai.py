"""
AI Routes
Handles AI assistant chat, reports, and intelligent insights
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
import json
from app import db
from app.models.ai import ChatMessage, AIReport
from app.models.meal import Meal
from app.models.habit import Habit
from app.models.expense import Expense
from app.models.goal import Goal
from app.services.ai_service import AIService

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')


# ==================== CHAT ROUTES ====================

@ai_bp.route('/chat')
@login_required
def chat_dashboard():
    """Display AI chat interface"""
    page = request.args.get('page', 1, type=int)
    messages = ChatMessage.query.filter_by(user_id=current_user.id).order_by(
        ChatMessage.created_at.desc()
    ).paginate(page=page, per_page=20)

    return render_template('ai/chat.html', messages=messages)


@ai_bp.route('/api/chat', methods=['POST'])
@login_required
def send_message():
    """Send message to AI and get response"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        topic = data.get('topic', 'general')  # general, finance, health, habits

        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Save user message
        user_msg = ChatMessage(
            user_id=current_user.id,
            message_type='user',
            content=user_message,
            topic=topic
        )
        db.session.add(user_msg)
        db.session.commit()

        # Gather context data based on topic
        context_data = {}

        if topic in ['finance', 'general']:
            expenses = Expense.query.filter_by(user_id=current_user.id).order_by(
                Expense.expense_date.desc()
            ).limit(10).all()
            context_data['expenses'] = f"{len(expenses)} recent expenses totaling ${sum(e.amount for e in expenses):.2f}"

        if topic in ['health', 'general']:
            meals = Meal.query.filter_by(user_id=current_user.id).order_by(
                Meal.meal_date.desc()
            ).limit(5).all()
            habits = Habit.query.filter_by(user_id=current_user.id).limit(5).all()
            context_data['meals'] = f"{len(meals)} recent meals logged"
            context_data['habits'] = f"{len(habits)} active habits"

        # Get AI response
        ai_response = AIService.chat_with_gemini(user_message, current_user.id, context_data)

        # Save AI message
        ai_msg = ChatMessage(
            user_id=current_user.id,
            message_type='assistant',
            content=ai_response,
            topic=topic
        )
        db.session.add(ai_msg)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'response': ai_response,
            'message_id': ai_msg.id,
            'timestamp': ai_msg.created_at.isoformat()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/chat-history')
@login_required
def chat_history():
    """View chat history"""
    page = request.args.get('page', 1, type=int)
    topic = request.args.get('topic', None)

    query = ChatMessage.query.filter_by(user_id=current_user.id)

    if topic:
        query = query.filter_by(topic=topic)

    messages = query.order_by(ChatMessage.created_at.desc()).paginate(page=page, per_page=50)

    return render_template('ai/chat_history.html', messages=messages, selected_topic=topic)


@ai_bp.route('/chat/<int:message_id>/delete', methods=['POST'])
@login_required
def delete_message(message_id):
    """Delete a chat message"""
    message = ChatMessage.query.get_or_404(message_id)

    if message.user_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('ai.chat_dashboard'))

    db.session.delete(message)
    db.session.commit()
    flash('Message deleted', 'success')
    return redirect(url_for('ai.chat_dashboard'))


# ==================== INSIGHTS & REPORTS ROUTES ====================

@ai_bp.route('/insights')
@login_required
def insights_dashboard():
    """Display AI-generated insights"""
    financial = AIService.get_financial_insights(current_user.id)
    health = AIService.get_health_insights(current_user.id)
    habits = AIService.analyze_habit_consistency(current_user.id)
    expense_pred = AIService.predict_expenses(current_user.id)

    return render_template('ai/insights.html',
                          financial=financial,
                          health=health,
                          habits=habits,
                          expense_prediction=expense_pred)


@ai_bp.route('/api/insights/financial', methods=['GET'])
@login_required
def get_financial_insights_api():
    """Get financial insights (API)"""
    insights = AIService.get_financial_insights(current_user.id)
    return jsonify(insights)


@ai_bp.route('/api/insights/health', methods=['GET'])
@login_required
def get_health_insights_api():
    """Get health insights (API)"""
    insights = AIService.get_health_insights(current_user.id)
    return jsonify(insights)


@ai_bp.route('/api/insights/habits', methods=['GET'])
@login_required
def get_habits_insights_api():
    """Get habits insights (API)"""
    insights = AIService.analyze_habit_consistency(current_user.id)
    return jsonify(insights)


@ai_bp.route('/api/predictions/expenses', methods=['GET'])
@login_required
def predict_expenses_api():
    """Get expense prediction (API)"""
    days = request.args.get('days', 30, type=int)
    prediction = AIService.predict_expenses(current_user.id, days_ahead=days)
    return jsonify(prediction)


# ==================== REPORTS ROUTES ====================

@ai_bp.route('/reports')
@login_required
def reports_dashboard():
    """Display AI reports"""
    page = request.args.get('page', 1, type=int)
    reports = AIReport.query.filter_by(user_id=current_user.id).order_by(
        AIReport.report_date.desc()
    ).paginate(page=page, per_page=5)

    return render_template('ai/reports.html', reports=reports)


@ai_bp.route('/report/generate', methods=['POST'])
@login_required
def generate_report():
    """Generate a new weekly report"""
    try:
        report_data = AIService.generate_weekly_report(current_user.id)

        if 'error' in report_data:
            flash(f'Error generating report: {report_data["error"]}', 'danger')
            return redirect(url_for('ai.reports_dashboard'))

        # Safely extract and JSON-serialize the data
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
        if not ai_summary or (isinstance(ai_summary, str) and len(ai_summary.strip()) == 0):
            ai_summary = "Your weekly report is ready. Check back for AI-generated insights!"

        # Save report to database
        report = AIReport(
            user_id=current_user.id,
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

        flash('Weekly report generated successfully!', 'success')
        return redirect(url_for('ai.reports_dashboard'))

    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        flash(f'Error generating report: {str(e)}', 'danger')
        return redirect(url_for('ai.reports_dashboard'))


@ai_bp.route('/report/<int:report_id>')
@login_required
def view_report(report_id):
    """View a specific report"""
    report = AIReport.query.get_or_404(report_id)

    if report.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('ai.reports_dashboard'))

    return render_template('ai/report_view.html', report=report)


@ai_bp.route('/report/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_report(report_id):
    """Delete a report"""
    report = AIReport.query.get_or_404(report_id)

    if report.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('ai.reports_dashboard'))

    title = report.title
    db.session.delete(report)
    db.session.commit()

    flash(f'Report "{title}" deleted', 'success')
    return redirect(url_for('ai.reports_dashboard'))


# ==================== API SUMMARY ROUTES ====================

@ai_bp.route('/api/summary', methods=['GET'])
@login_required
def get_summary_api():
    """Get complete AI summary (API)"""
    return jsonify({
        'financial_insights': AIService.get_financial_insights(current_user.id),
        'health_insights': AIService.get_health_insights(current_user.id),
        'habit_analysis': AIService.analyze_habit_consistency(current_user.id),
        'expense_prediction': AIService.predict_expenses(current_user.id),
        'generated_at': datetime.utcnow().isoformat()
    })


# ==================== REPORTS API ROUTES ====================

@ai_bp.route('/api/report/generate', methods=['POST'])
@login_required
def generate_report_api():
    """API endpoint to generate weekly report (AJAX)"""
    try:
        report_data = AIService.generate_weekly_report(current_user.id)

        if 'error' in report_data:
            return jsonify({'status': 'error', 'message': report_data["error"]}), 400

        # Safely serialize data
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
            ai_summary = "Your weekly report is ready!"

        # Save report
        report = AIReport(
            user_id=current_user.id,
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

        return jsonify({
            'status': 'success',
            'report_id': report.id,
            'message': 'Weekly report generated successfully!',
            'redirect': url_for('ai.view_report', report_id=report.id)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@ai_bp.route('/api/report/check-data', methods=['GET'])
@login_required
def check_report_data():
    """Check if user has enough data for report generation"""
    try:
        expenses = Expense.query.filter_by(user_id=current_user.id).count()
        meals = Meal.query.filter_by(user_id=current_user.id).count()
        habits = Habit.query.filter_by(user_id=current_user.id).count()

        has_expenses = expenses > 0
        has_meals = meals > 0
        has_habits = habits > 0
        has_any_data = has_expenses or has_meals or has_habits

        return jsonify({
            'status': 'success',
            'has_data': has_any_data,
            'expenses': expenses,
            'meals': meals,
            'habits': habits,
            'data_summary': {
                'expenses': 'Yes' if has_expenses else 'No - Log some expenses',
                'meals': 'Yes' if has_meals else 'No - Log some meals',
                'habits': 'Yes' if has_habits else 'No - Create some habits'
            },
            'can_generate': has_any_data
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@ai_bp.route('/api/reports/recent', methods=['GET'])
@login_required
def get_recent_reports():
    """Get recent reports (API)"""
    try:
        limit = request.args.get('limit', 5, type=int)
        reports = AIReport.query.filter_by(user_id=current_user.id).order_by(
            AIReport.report_date.desc()
        ).limit(limit).all()

        return jsonify({
            'status': 'success',
            'count': len(reports),
            'reports': [
                {
                    'id': r.id,
                    'title': r.title,
                    'report_date': r.report_date.isoformat(),
                    'preview': r.content[:100] + '...' if len(r.content) > 100 else r.content
                }
                for r in reports
            ]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

