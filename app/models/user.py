"""
User Model
Represents the core user entity with authentication and profile information
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    """
    User Model with authentication capabilities
    Includes profile data and account management
    """
    __tablename__ = 'users'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Authentication & Identity
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profile Information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.Text)

    # Contact Information
    phone = db.Column(db.String(15))
    location = db.Column(db.String(200))

    # Account Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Goals & Preferences
    monthly_budget = db.Column(db.Float, default=0.0)
    weight_goal = db.Column(db.Float)  # in kg
    savings_goal = db.Column(db.Float)  # in currency
    daily_calorie_goal = db.Column(db.Integer, default=2000)
    daily_protein_goal = db.Column(db.Float, default=50.0)  # in grams

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)

    # Relationships
    expenses = db.relationship('Expense', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    meals = db.relationship('Meal', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    habits = db.relationship('Habit', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    goals = db.relationship('Goal', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    groceries = db.relationship('GroceryItem', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against hash"""
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        """Convert user to dictionary for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'profile_picture': self.profile_picture,
            'bio': self.bio,
            'phone': self.phone,
            'location': self.location,
            'is_admin': self.is_admin,
            'monthly_budget': self.monthly_budget,
            'weight_goal': self.weight_goal,
            'savings_goal': self.savings_goal,
            'daily_calorie_goal': self.daily_calorie_goal,
            'daily_protein_goal': self.daily_protein_goal,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

