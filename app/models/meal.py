"""
Meal Model
Tracks meal logging and nutritional information
"""
from datetime import datetime
from app import db

class Meal(db.Model):
    """
    Meal Model
    Logs meals with nutritional details
    """
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Meal Information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # Nutritional Details
    calories = db.Column(db.Float, nullable=False, default=0)
    protein = db.Column(db.Float, default=0)  # in grams
    carbs = db.Column(db.Float, default=0)    # in grams
    fat = db.Column(db.Float, default=0)      # in grams

    # Meal Type
    meal_type = db.Column(db.String(50))  # breakfast, lunch, dinner, snack

    # Timestamps
    meal_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = db.relationship('User', back_populates='meals')

    def __repr__(self):
        return f'<Meal {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'meal_type': self.meal_type,
            'meal_date': self.meal_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }

