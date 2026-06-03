"""
Grocery Routes
Handles grocery management and shopping lists
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.grocery import GroceryItem
from app.services.grocery_service import GroceryService

grocery_bp = Blueprint('grocery', __name__, url_prefix='/grocery')


@grocery_bp.route('/dashboard')
@login_required
def dashboard():
    """Grocery dashboard"""
    shopping_list = GroceryService.get_shopping_list(current_user.id)
    shopping_total = GroceryService.get_shopping_list_total(current_user.id)
    category_breakdown = GroceryService.get_category_breakdown(current_user.id, purchased=False)

    return render_template('grocery/dashboard.html',
                         shopping_list=shopping_list,
                         shopping_total=shopping_total,
                         category_breakdown=category_breakdown)


@grocery_bp.route('/shopping-list')
@login_required
def shopping_list():
    """Shopping list page"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '').strip()
    sort_by = request.args.get('sort', 'created')

    query = GroceryItem.query.filter_by(user_id=current_user.id, is_purchased=False)

    if category:
        query = query.filter_by(category=category)

    # Sorting
    if sort_by == 'name':
        query = query.order_by(GroceryItem.name.asc())
    elif sort_by == 'price_high':
        query = query.order_by(GroceryItem.price.desc())
    elif sort_by == 'price_low':
        query = query.order_by(GroceryItem.price.asc())
    else:
        query = query.order_by(GroceryItem.created_at.desc())

    items = query.paginate(page=page, per_page=20)

    # Get unique categories
    categories = db.session.query(GroceryItem.category).filter(
        GroceryItem.user_id == current_user.id,
        GroceryItem.is_purchased == False,
        GroceryItem.category != ''
    ).distinct().all()
    categories = [c[0] for c in categories]

    total = GroceryService.get_shopping_list_total(current_user.id)

    return render_template('grocery/shopping_list.html',
                         items=items,
                         total=total,
                         categories=categories,
                         selected_category=category,
                         sort_by=sort_by)


@grocery_bp.route('/item/add', methods=['GET', 'POST'])
@login_required
def add_item():
    """Add grocery item"""
    if request.method == 'POST':
        data = request.form

        # Robust parsing: allow users to enter '2 kg' in the quantity field
        def _parse_quantity_field(raw):
            raw = (raw or '').strip()
            try:
                return float(raw), None
            except ValueError:
                import re
                m = re.match(r'^([0-9]*\.?[0-9]+)\s*(.*)$', raw)
                if m:
                    q = float(m.group(1))
                    unit_part = (m.group(2) or '').strip()
                    return q, unit_part or None
                raise

        try:
            raw_q = data.get('quantity', '1')
            quantity, unit_from_q = _parse_quantity_field(raw_q)
            price = float(data.get('price', 0))
        except Exception:
            flash('Invalid quantity or price!', 'error')
            return redirect(url_for('grocery.add_item'))

        try:
            unit_field = data.get('unit', '').strip()
            unit = unit_field or unit_from_q or ''

            item = GroceryService.create_grocery_item(
                user_id=current_user.id,
                name=data.get('name', '').strip(),
                quantity=quantity,
                unit=unit,
                price=price,
                category=data.get('category', '').strip(),
                description=data.get('description', '').strip()
            )
            flash('Grocery item added successfully!', 'success')
            return redirect(url_for('grocery.shopping_list'))
        except Exception as e:
            flash(f'Failed to add item: {str(e)}', 'error')
            return redirect(url_for('grocery.add_item'))

    return render_template('grocery/add_item.html')


@grocery_bp.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    """Edit grocery item"""
    item = GroceryItem.query.get_or_404(item_id)

    # Check ownership
    if item.user_id != current_user.id:
        flash('You do not have permission to edit this item!', 'error')
        return redirect(url_for('grocery.shopping_list'))

    if request.method == 'POST':
        data = request.form

        # Robust parsing for edit as well (accept '2 kg' in quantity)
        def _parse_quantity_field(raw):
            raw = (raw or '').strip()
            try:
                return float(raw), None
            except ValueError:
                import re
                m = re.match(r'^([0-9]*\.?[0-9]+)\s*(.*)$', raw)
                if m:
                    q = float(m.group(1))
                    unit_part = (m.group(2) or '').strip()
                    return q, unit_part or None
                raise

        try:
            raw_q = data.get('quantity', str(item.quantity))
            quantity, unit_from_q = _parse_quantity_field(raw_q)
            price = float(data.get('price', item.price))
        except Exception:
            flash('Invalid quantity or price!', 'error')
            return redirect(url_for('grocery.edit_item', item_id=item_id))

        try:
            unit_field = data.get('unit', '').strip()
            unit = unit_field or unit_from_q or item.unit or ''

            GroceryService.update_grocery_item(
                item_id,
                name=data.get('name', '').strip(),
                quantity=quantity,
                unit=unit,
                price=price,
                category=data.get('category', '').strip(),
                description=data.get('description', '').strip()
            )
            flash('Grocery item updated successfully!', 'success')
            return redirect(url_for('grocery.shopping_list'))
        except Exception as e:
            flash(f'Failed to update item: {str(e)}', 'error')
            return redirect(url_for('grocery.edit_item', item_id=item_id))

    return render_template('grocery/edit_item.html', item=item)


@grocery_bp.route('/item/<int:item_id>/toggle', methods=['POST'])
@login_required
def toggle_item(item_id):
    """Toggle item purchase status"""
    item = GroceryItem.query.get_or_404(item_id)

    # Check ownership
    if item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        if item.is_purchased:
            GroceryService.mark_as_unpurchased(item_id)
        else:
            GroceryService.mark_as_purchased(item_id)

        return jsonify({'status': 'success', 'is_purchased': item.is_purchased})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@grocery_bp.route('/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    """Delete grocery item"""
    item = GroceryItem.query.get_or_404(item_id)

    # Check ownership
    if item.user_id != current_user.id:
        flash('You do not have permission to delete this item!', 'error')
        return redirect(url_for('grocery.shopping_list'))

    try:
        GroceryService.delete_grocery_item(item_id)
        flash('Grocery item deleted successfully!', 'success')
    except Exception as e:
        flash(f'Failed to delete item: {str(e)}', 'error')

    return redirect(url_for('grocery.shopping_list'))


@grocery_bp.route('/history')
@login_required
def history():
    """Purchased items history"""
    page = request.args.get('page', 1, type=int)

    query = GroceryItem.query.filter_by(user_id=current_user.id, is_purchased=True)
    items = query.order_by(GroceryItem.purchase_date.desc()).paginate(page=page, per_page=20)

    return render_template('grocery/history.html', items=items)


# API Endpoints
@grocery_bp.route('/api/shopping-list', methods=['GET'])
@login_required
def api_shopping_list():
    """API: Get shopping list"""
    items = GroceryService.get_shopping_list(current_user.id)
    return jsonify([item.to_dict() for item in items])


@grocery_bp.route('/api/shopping-total', methods=['GET'])
@login_required
def api_shopping_total():
    """API: Get shopping list total"""
    total = GroceryService.get_shopping_list_total(current_user.id)
    return jsonify({'total': total})


@grocery_bp.route('/api/items/bulk-mark', methods=['POST'])
@login_required
def api_bulk_mark():
    """API: Bulk mark items as purchased"""
    data = request.get_json()
    item_ids = data.get('item_ids', [])

    try:
        count = GroceryService.bulk_mark_purchased(current_user.id, item_ids)
        return jsonify({'status': 'success', 'count': count})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

