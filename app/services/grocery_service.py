"""
Grocery Service
Business logic for grocery management and shopping lists
"""
from datetime import datetime
from sqlalchemy import func
from app import db
from app.models.grocery import GroceryItem


class GroceryService:
    """Service for grocery operations"""

    @staticmethod
    def create_grocery_item(user_id, name, quantity, unit, price, category='', description=''):
        """
        Create a new grocery item

        Args:
            user_id: User ID
            name: Item name
            quantity: Item quantity
            unit: Unit of measurement (kg, liters, etc)
            price: Item price
            category: Item category
            description: Optional description

        Returns:
            GroceryItem object or None
        """
        try:
            item = GroceryItem(
                user_id=user_id,
                name=name,
                quantity=quantity,
                unit=unit,
                price=price,
                category=category,
                description=description,
                is_purchased=False
            )
            db.session.add(item)
            db.session.commit()
            return item
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to create grocery item: {str(e)}")

    @staticmethod
    def get_user_grocery_items(user_id, purchased=None):
        """
        Get grocery items for user

        Args:
            user_id: User ID
            purchased: Filter by purchase status (None = all)

        Returns:
            List of grocery items
        """
        query = GroceryItem.query.filter_by(user_id=user_id)

        if purchased is not None:
            query = query.filter_by(is_purchased=purchased)

        return query.order_by(GroceryItem.created_at.desc()).all()

    @staticmethod
    def get_shopping_list(user_id):
        """
        Get unpurchased grocery items (shopping list)

        Args:
            user_id: User ID

        Returns:
            List of unpurchased items
        """
        return GroceryService.get_user_grocery_items(user_id, purchased=False)

    @staticmethod
    def get_purchased_items(user_id):
        """
        Get purchased grocery items

        Args:
            user_id: User ID

        Returns:
            List of purchased items
        """
        return GroceryService.get_user_grocery_items(user_id, purchased=True)

    @staticmethod
    def mark_as_purchased(item_id):
        """
        Mark grocery item as purchased

        Args:
            item_id: Item ID

        Returns:
            Updated item or None
        """
        try:
            item = GroceryItem.query.get(item_id)
            if not item:
                return None

            item.is_purchased = True
            item.purchase_date = datetime.utcnow()
            db.session.commit()
            return item
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to mark item as purchased: {str(e)}")

    @staticmethod
    def mark_as_unpurchased(item_id):
        """
        Mark grocery item as unpurchased

        Args:
            item_id: Item ID

        Returns:
            Updated item or None
        """
        try:
            item = GroceryItem.query.get(item_id)
            if not item:
                return None

            item.is_purchased = False
            item.purchase_date = None
            db.session.commit()
            return item
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to mark item as unpurchased: {str(e)}")

    @staticmethod
    def get_shopping_list_total(user_id):
        """
        Get total cost of unpurchased items

        Args:
            user_id: User ID

        Returns:
            Total cost
        """
        result = db.session.query(
            func.sum(GroceryItem.quantity * GroceryItem.price)
        ).filter(
            GroceryItem.user_id == user_id,
            GroceryItem.is_purchased == False
        ).scalar()

        return float(result) if result else 0.0

    @staticmethod
    def get_category_breakdown(user_id, purchased=None):
        """
        Get grocery items breakdown by category

        Args:
            user_id: User ID
            purchased: Filter by purchase status

        Returns:
            Dictionary of category: total_cost
        """
        query = db.session.query(
            GroceryItem.category,
            func.sum(GroceryItem.quantity * GroceryItem.price).label('total')
        ).filter(GroceryItem.user_id == user_id)

        if purchased is not None:
            query = query.filter(GroceryItem.is_purchased == purchased)

        results = query.group_by(GroceryItem.category).all()

        return {category: float(total) for category, total in results if category}

    @staticmethod
    def update_grocery_item(item_id, **kwargs):
        """
        Update a grocery item

        Args:
            item_id: Item ID
            **kwargs: Fields to update

        Returns:
            Updated item or None
        """
        try:
            item = GroceryItem.query.get(item_id)
            if not item:
                return None

            for key, value in kwargs.items():
                if hasattr(item, key) and key not in ['id', 'user_id', 'created_at']:
                    setattr(item, key, value)

            db.session.commit()
            return item
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update grocery item: {str(e)}")

    @staticmethod
    def delete_grocery_item(item_id):
        """
        Delete a grocery item

        Args:
            item_id: Item ID

        Returns:
            True if deleted, False otherwise
        """
        try:
            item = GroceryItem.query.get(item_id)
            if not item:
                return False

            db.session.delete(item)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to delete grocery item: {str(e)}")

    @staticmethod
    def bulk_mark_purchased(user_id, item_ids):
        """
        Mark multiple items as purchased

        Args:
            user_id: User ID
            item_ids: List of item IDs

        Returns:
            Number of items updated
        """
        try:
            count = GroceryItem.query.filter(
                GroceryItem.user_id == user_id,
                GroceryItem.id.in_(item_ids)
            ).update({
                GroceryItem.is_purchased: True,
                GroceryItem.purchase_date: datetime.utcnow()
            })
            db.session.commit()
            return count
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to bulk update items: {str(e)}")

