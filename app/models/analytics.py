"""
Analytics Model
Stores user analytics data and Life Score calculations
"""
from datetime import datetime
from app import db

class LifeScore(db.Model):
    """
    Life Score Model
    Stores calculated life score and component scores
    """
    __tablename__ = 'life_scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Overall Score
    overall_score = db.Column(db.Float, default=0)  # 0-100

    # Component Scores (0-100)
    health_score = db.Column(db.Float, default=0)
    financial_score = db.Column(db.Float, default=0)
    habit_score = db.Column(db.Float, default=0)

    # Score Details
    health_discipline = db.Column(db.Float, default=0)  # Based on calorie tracking consistency
    financial_discipline = db.Column(db.Float, default=0)  # Based on budget adherence
    habit_consistency = db.Column(db.Float, default=0)  # Based on habit completion rates

    # Metadata
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref=db.backref('life_scores', cascade='all, delete-orphan', lazy='dynamic'))

    def __repr__(self):
        return f'<LifeScore User={self.user_id} Score={self.overall_score}>'

    def to_dict(self):
        return {
            'id': self.id,
            'overall_score': self.overall_score,
            'health_score': self.health_score,
            'financial_score': self.financial_score,
            'habit_score': self.habit_score,
            'health_discipline': self.health_discipline,
            'financial_discipline': self.financial_discipline,
            'habit_consistency': self.habit_consistency,
            'calculated_at': self.calculated_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class UserBudget(db.Model):
    """
    User Budget Model
    Stores user's monthly budget limit
    """
    __tablename__ = 'user_budgets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)

    # Budget Settings
    monthly_limit = db.Column(db.Float, default=3000)  # Default $3000/month
    alert_threshold = db.Column(db.Float, default=90)  # Alert at 90% of budget

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref=db.backref('budget', uselist=False))

    def __repr__(self):
        return f'<UserBudget User={self.user_id} Limit={self.monthly_limit}>'

    def to_dict(self):
        return {
            'id': self.id,
            'monthly_limit': self.monthly_limit,
            'alert_threshold': self.alert_threshold,
            'created_at': self.created_at.isoformat()
        }

