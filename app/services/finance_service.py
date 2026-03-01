"""
Finance Service
Business logic for expense tracking and budget management
"""
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from app import db
from app.models.expense import Expense, ExpenseCategory
from app.models.user import User


class FinanceService:
    """Service for financial operations"""

    @staticmethod
    def create_expense(user_id, title, amount, category_id, description='', expense_date=None):
        """
        Create a new expense

        Args:
            user_id: User ID
            title: Expense title
            amount: Expense amount
            category_id: Category ID
            description: Optional description
            expense_date: Date of expense (defaults to today)

        Returns:
            Expense object or None if error
        """
        try:
            if not expense_date:
                expense_date = datetime.utcnow()

            expense = Expense(
                user_id=user_id,
                title=title,
                amount=amount,
                category_id=category_id,
                description=description,
                expense_date=expense_date
            )
            db.session.add(expense)
            db.session.commit()
            return expense
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to create expense: {str(e)}")

    @staticmethod
    def get_user_expenses(user_id, start_date=None, end_date=None, category_id=None):
        """
        Get user expenses with optional filtering

        Args:
            user_id: User ID
            start_date: Start date filter
            end_date: End date filter
            category_id: Category filter

        Returns:
            List of expenses
        """
        query = Expense.query.filter_by(user_id=user_id)

        if start_date:
            query = query.filter(Expense.expense_date >= start_date)

        if end_date:
            query = query.filter(Expense.expense_date <= end_date)

        if category_id:
            query = query.filter_by(category_id=category_id)

        return query.order_by(Expense.expense_date.desc()).all()

    @staticmethod
    def get_monthly_expenses(user_id, year=None, month=None):
        """
        Get expenses for a specific month

        Args:
            user_id: User ID
            year: Year (defaults to current)
            month: Month (defaults to current)

        Returns:
            List of monthly expenses
        """
        if not year:
            year = datetime.utcnow().year
        if not month:
            month = datetime.utcnow().month

        return Expense.query.filter(
            Expense.user_id == user_id,
            extract('year', Expense.expense_date) == year,
            extract('month', Expense.expense_date) == month
        ).all()

    @staticmethod
    def get_monthly_total(user_id, year=None, month=None):
        """
        Get total expenses for a month

        Args:
            user_id: User ID
            year: Year
            month: Month

        Returns:
            Total amount
        """
        if not year:
            year = datetime.utcnow().year
        if not month:
            month = datetime.utcnow().month

        result = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == user_id,
            extract('year', Expense.expense_date) == year,
            extract('month', Expense.expense_date) == month
        ).scalar()

        return float(result) if result else 0.0

    @staticmethod
    def get_category_breakdown(user_id, start_date=None, end_date=None):
        """
        Get expense breakdown by category

        Args:
            user_id: User ID
            start_date: Start date
            end_date: End date

        Returns:
            Dictionary of category: total_amount
        """
        query = db.session.query(
            ExpenseCategory.name,
            func.sum(Expense.amount).label('total')
        ).join(Expense).filter(Expense.user_id == user_id)

        if start_date:
            query = query.filter(Expense.expense_date >= start_date)

        if end_date:
            query = query.filter(Expense.expense_date <= end_date)

        results = query.group_by(ExpenseCategory.id).all()

        return {name: float(total) for name, total in results}

    @staticmethod
    def check_budget_status(user_id, year=None, month=None):
        """
        Check user's budget status for the month

        Args:
            user_id: User ID
            year: Year
            month: Month

        Returns:
            Dictionary with budget info
        """
        user = User.query.get(user_id)
        if not user:
            return None

        monthly_total = FinanceService.get_monthly_total(user_id, year, month)
        budget = user.monthly_budget

        return {
            'budget': budget,
            'spent': monthly_total,
            'remaining': budget - monthly_total,
            'percentage_used': (monthly_total / budget * 100) if budget > 0 else 0,
            'is_over_budget': monthly_total > budget
        }

    @staticmethod
    def get_spending_trends(user_id, months=6):
        """
        Get spending trends over last N months

        Args:
            user_id: User ID
            months: Number of months to analyze

        Returns:
            List of monthly spending data
        """
        trends = []

        for i in range(months - 1, -1, -1):
            date = datetime.utcnow() - timedelta(days=30 * i)
            year = date.year
            month = date.month

            total = FinanceService.get_monthly_total(user_id, year, month)
            trends.append({
                'year': year,
                'month': month,
                'month_name': date.strftime('%B'),
                'total': total
            })

        return trends

    @staticmethod
    def update_expense(expense_id, **kwargs):
        """
        Update an expense

        Args:
            expense_id: Expense ID
            **kwargs: Fields to update

        Returns:
            Updated expense or None
        """
        try:
            expense = Expense.query.get(expense_id)
            if not expense:
                return None

            for key, value in kwargs.items():
                if hasattr(expense, key):
                    setattr(expense, key, value)

            db.session.commit()
            return expense
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update expense: {str(e)}")

    @staticmethod
    def delete_expense(expense_id):
        """
        Delete an expense

        Args:
            expense_id: Expense ID

        Returns:
            True if deleted, False otherwise
        """
        try:
            expense = Expense.query.get(expense_id)
            if not expense:
                return False

            db.session.delete(expense)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to delete expense: {str(e)}")

