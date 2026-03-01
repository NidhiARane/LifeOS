"""
Helper Functions
Utility functions for common operations
"""
from datetime import datetime, timedelta
from flask import render_template_string


def format_date(date_obj, format_str='%Y-%m-%d'):
    """Format datetime object to string"""
    if not date_obj:
        return ''
    return date_obj.strftime(format_str)


def format_currency(amount, currency='USD', decimals=2):
    """Format amount as currency"""
    currency_symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'INR': '₹',
        'JPY': '¥'
    }
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol}{amount:,.{decimals}f}"


def get_date_range(days=30):
    """Get date range for last N days"""
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def calculate_age(birth_date):
    """Calculate age from birth date"""
    today = datetime.utcnow().date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def get_greeting():
    """Get time-based greeting"""
    hour = datetime.utcnow().hour
    if hour < 12:
        return 'Good Morning'
    elif hour < 18:
        return 'Good Afternoon'
    else:
        return 'Good Evening'


def paginate_data(query, page=1, per_page=20):
    """Paginate database query"""
    return query.paginate(page=page, per_page=per_page)


def humanize_datetime(dt):
    """Convert datetime to human-readable format"""
    if not dt:
        return 'Never'

    now = datetime.utcnow()
    diff = now - dt

    if diff.days == 0:
        if diff.seconds < 60:
            return 'Just now'
        elif diff.seconds < 3600:
            minutes = diff.seconds // 60
            return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
        else:
            hours = diff.seconds // 3600
            return f'{hours} hour{"s" if hours > 1 else ""} ago'
    elif diff.days == 1:
        return 'Yesterday'
    elif diff.days < 7:
        return f'{diff.days} days ago'
    elif diff.days < 30:
        weeks = diff.days // 7
        return f'{weeks} week{"s" if weeks > 1 else ""} ago'
    else:
        return dt.strftime('%B %d, %Y')

