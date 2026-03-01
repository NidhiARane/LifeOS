"""
Grocery Model
Tracks grocery items and shopping
"""
from datetime import datetime
from app import db

class GroceryItem(db.Model):
    """
    Grocery Item Model
    Tracks grocery items with pricing and quantity
    """
    __tablename__ = 'grocery_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Item Details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # vegetables, fruits, dairy, etc.

    # Pricing & Quantity
    quantity = db.Column(db.Float, nullable=False, default=1)
    unit = db.Column(db.String(50))  # kg, liters, pieces, etc.
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')

    # Tracking
    is_purchased = db.Column(db.Boolean, default=False)
    purchase_date = db.Column(db.DateTime)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = db.relationship('User', back_populates='groceries')

    def __repr__(self):
        return f'<GroceryItem {self.name}>'

    def get_total_cost(self):
        """Calculate total cost"""
        return self.quantity * self.price

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'quantity': self.quantity,
            'unit': self.unit,
            'price': self.price,
            'currency': self.currency,
            'total_cost': self.get_total_cost(),
            'is_purchased': self.is_purchased,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'created_at': self.created_at.isoformat()
        }

