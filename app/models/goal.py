"""
Goal Model
Tracks user goals across different life areas
"""
from datetime import datetime
from app import db

class Goal(db.Model):
    """
    Goal Model
    Represents user goals with progress tracking
    """
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Goal Details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # health, financial, learning, fitness, etc.

    # Goal Progress
    target_value = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, default=0)
    unit = db.Column(db.String(50))  # kg, $, books, hours, etc.

    # Timeline
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    target_date = db.Column(db.DateTime)

    # Status
    is_completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    # Relationship
    user = db.relationship('User', back_populates='goals')

    def __repr__(self):
        return f'<Goal {self.title}>'

    def get_progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_value == 0:
            return 0
        return min((self.current_value / self.target_value) * 100, 100)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'unit': self.unit,
            'progress_percentage': self.get_progress_percentage(),
            'is_completed': self.is_completed,
            'priority': self.priority,
            'start_date': self.start_date.isoformat(),
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'created_at': self.created_at.isoformat()
        }

