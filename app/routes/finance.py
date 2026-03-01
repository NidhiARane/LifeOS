"""
Finance Routes
Handles expense tracking and budget management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.expense import Expense, ExpenseCategory
from app.services.finance_service import FinanceService
from app.services.ai_suggestions_service import AISuggestionsService

finance_bp = Blueprint('finance', __name__, url_prefix='/finance')


def init_expense_categories():
    """Initialize default expense categories if they don't exist"""
    categories = [
        ('Food & Dining', '#FF6B6B', 'fas fa-utensils'),
        ('Transportation', '#4ECDC4', 'fas fa-car'),
        ('Utilities', '#95E1D3', 'fas fa-lightbulb'),
        ('Entertainment', '#FFD93D', 'fas fa-film'),
        ('Shopping', '#6BCB77', 'fas fa-shopping-bag'),
        ('Healthcare', '#FF6B9D', 'fas fa-hospital'),
        ('Education', '#4D96FF', 'fas fa-book'),
        ('Other', '#A8A8A8', 'fas fa-tag')
    ]

    for name, color, icon in categories:
        if not ExpenseCategory.query.filter_by(name=name).first():
            category = ExpenseCategory(name=name, color=color, icon=icon)
            db.session.add(category)

    db.session.commit()


@finance_bp.route('/dashboard')
@login_required
def dashboard():
    """Finance dashboard"""
    # Initialize categories on first visit
    init_expense_categories()

    # Get current month budget status
    budget_status = FinanceService.check_budget_status(current_user.id)

    # Get current month expenses
    current_month_expenses = FinanceService.get_monthly_expenses(current_user.id)

    # Get spending trends
    trends = FinanceService.get_spending_trends(current_user.id, months=6)

    # Get category breakdown
    category_breakdown = FinanceService.get_category_breakdown(current_user.id)

    # Get AI suggestions
    suggestions = AISuggestionsService.get_saving_suggestions(current_user.id)
    budget_insights = AISuggestionsService.get_budget_insights(current_user.id)

    return render_template('finance/dashboard.html',
                         budget_status=budget_status,
                         expenses=current_month_expenses,
                         trends=trends,
                         category_breakdown=category_breakdown,
                         suggestions=suggestions,
                         budget_insights=budget_insights)


@finance_bp.route('/expenses')
@login_required
def expenses():
    """View all expenses"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', None, type=int)
    sort_by = request.args.get('sort', 'date_desc')

    query = Expense.query.filter_by(user_id=current_user.id)

    if category_id:
        query = query.filter_by(category_id=category_id)

    # Sorting
    if sort_by == 'date_asc':
        query = query.order_by(Expense.expense_date.asc())
    elif sort_by == 'amount_desc':
        query = query.order_by(Expense.amount.desc())
    elif sort_by == 'amount_asc':
        query = query.order_by(Expense.amount.asc())
    else:
        query = query.order_by(Expense.expense_date.desc())

    expenses = query.paginate(page=page, per_page=20)
    categories = ExpenseCategory.query.all()

    return render_template('finance/expenses.html',
                         expenses=expenses,
                         categories=categories,
                         selected_category=category_id,
                         sort_by=sort_by)


@finance_bp.route('/expense/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add new expense"""
    if request.method == 'POST':
        data = request.form

        try:
            expense_date = datetime.strptime(data.get('expense_date'), '%Y-%m-%d')
        except (ValueError, TypeError):
            expense_date = datetime.utcnow()

        try:
            amount = float(data.get('amount', 0))
        except ValueError:
            flash('Invalid amount!', 'error')
            return redirect(url_for('finance.add_expense'))

        try:
            expense = FinanceService.create_expense(
                user_id=current_user.id,
                title=data.get('title', '').strip(),
                amount=amount,
                category_id=int(data.get('category_id')),
                description=data.get('description', '').strip(),
                expense_date=expense_date
            )
            flash('Expense added successfully!', 'success')
            return redirect(url_for('finance.expenses'))
        except Exception as e:
            flash(f'Failed to add expense: {str(e)}', 'error')
            return redirect(url_for('finance.add_expense'))

    categories = ExpenseCategory.query.all()
    return render_template('finance/add_expense.html',
                         categories=categories,
                         now=datetime.utcnow())


@finance_bp.route('/expense/<int:expense_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """Edit expense"""
    expense = Expense.query.get_or_404(expense_id)

    # Check ownership
    if expense.user_id != current_user.id:
        flash('You do not have permission to edit this expense!', 'error')
        return redirect(url_for('finance.expenses'))

    if request.method == 'POST':
        data = request.form

        try:
            expense_date = datetime.strptime(data.get('expense_date'), '%Y-%m-%d')
        except (ValueError, TypeError):
            expense_date = expense.expense_date

        try:
            amount = float(data.get('amount', expense.amount))
        except ValueError:
            flash('Invalid amount!', 'error')
            return redirect(url_for('finance.edit_expense', expense_id=expense_id))

        try:
            FinanceService.update_expense(
                expense_id,
                title=data.get('title', '').strip(),
                amount=amount,
                category_id=int(data.get('category_id')),
                description=data.get('description', '').strip(),
                expense_date=expense_date
            )
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('finance.expenses'))
        except Exception as e:
            flash(f'Failed to update expense: {str(e)}', 'error')
            return redirect(url_for('finance.edit_expense', expense_id=expense_id))

    categories = ExpenseCategory.query.all()
    return render_template('finance/edit_expense.html',
                         expense=expense,
                         categories=categories)


@finance_bp.route('/expense/<int:expense_id>/delete', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete expense"""
    expense = Expense.query.get_or_404(expense_id)

    # Check ownership
    if expense.user_id != current_user.id:
        flash('You do not have permission to delete this expense!', 'error')
        return redirect(url_for('finance.expenses'))

    try:
        FinanceService.delete_expense(expense_id)
        flash('Expense deleted successfully!', 'success')
    except Exception as e:
        flash(f'Failed to delete expense: {str(e)}', 'error')

    return redirect(url_for('finance.expenses'))


@finance_bp.route('/budget')
@login_required
def budget():
    """Budget management"""
    budget_status = FinanceService.check_budget_status(current_user.id)
    trends = FinanceService.get_spending_trends(current_user.id, months=12)
    category_breakdown = FinanceService.get_category_breakdown(current_user.id)

    return render_template('finance/budget.html',
                         budget_status=budget_status,
                         trends=trends,
                         category_breakdown=category_breakdown)


@finance_bp.route('/insights')
@login_required
def insights():
    """AI-powered insights"""
    suggestions = AISuggestionsService.get_saving_suggestions(current_user.id)
    budget_insights = AISuggestionsService.get_budget_insights(current_user.id)
    predictions = AISuggestionsService.get_expense_prediction(current_user.id, months_ahead=3)
    trends = FinanceService.get_spending_trends(current_user.id, months=6)

    return render_template('finance/insights.html',
                         suggestions=suggestions,
                         budget_insights=budget_insights,
                         predictions=predictions,
                         trends=trends)


# API Endpoints
@finance_bp.route('/api/expenses', methods=['GET'])
@login_required
def api_get_expenses():
    """API: Get expenses"""
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)

    if month and year:
        expenses = FinanceService.get_monthly_expenses(current_user.id, year, month)
    else:
        expenses = FinanceService.get_user_expenses(current_user.id)

    return jsonify([expense.to_dict() for expense in expenses])


@finance_bp.route('/api/budget-status', methods=['GET'])
@login_required
def api_budget_status():
    """API: Get budget status"""
    status = FinanceService.check_budget_status(current_user.id)
    return jsonify(status)


@finance_bp.route('/api/suggestions', methods=['GET'])
@login_required
def api_suggestions():
    """API: Get AI suggestions"""
    suggestions = AISuggestionsService.get_saving_suggestions(current_user.id)
    return jsonify(suggestions)

