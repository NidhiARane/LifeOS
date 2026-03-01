"""
Habit Model
Tracks user habits and their consistency
"""
from datetime import datetime
from app import db

class Habit(db.Model):
    """
    Habit Model
    Represents a habit with tracking capabilities
    """
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Habit Details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # health, productivity, learning, fitness, etc.

    # Tracking
    frequency = db.Column(db.String(50))  # daily, weekly, custom
    target = db.Column(db.Integer)  # number of times per week/month
    current_streak = db.Column(db.Integer, default=0)  # days/weeks
    longest_streak = db.Column(db.Integer, default=0)

    # Status
    is_active = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='habits')
    logs = db.relationship('HabitLog', back_populates='habit', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Habit {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'frequency': self.frequency,
            'target': self.target,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


class HabitLog(db.Model):
    """
    Habit Log Model
    Records completion of habit on specific dates
    """
    __tablename__ = 'habit_logs'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False, index=True)

    # Log Details
    completed_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    habit = db.relationship('Habit', back_populates='logs')

    def __repr__(self):
        return f'<HabitLog {self.habit_id} - {self.completed_date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'completed_date': self.completed_date.isoformat(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }

