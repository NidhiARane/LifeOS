"""
Expense Model
Tracks financial expenses with categorization
"""
from datetime import datetime
from app import db

class ExpenseCategory(db.Model):
    """Expense category enumeration"""
    __tablename__ = 'expense_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Icon class for UI
    color = db.Column(db.String(7), default='#FF5733')  # Hex color
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    expenses = db.relationship('Expense', back_populates='category')

    def __repr__(self):
        return f'<ExpenseCategory {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color
        }


class Expense(db.Model):
    """
    Expense Model
    Tracks individual expenses with amount, date, and category
    """
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('expense_categories.id'), nullable=False)

    # Expense Details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')

    # Timestamps
    expense_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='expenses')
    category = db.relationship('ExpenseCategory', back_populates='expenses')

    def __repr__(self):
        return f'<Expense {self.title} - {self.amount}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'amount': self.amount,
            'currency': self.currency,
            'category': self.category.to_dict() if self.category else None,
            'expense_date': self.expense_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

