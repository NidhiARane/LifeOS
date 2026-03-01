"""
Validators
Input validation functions
"""
import re
from email_validator import validate_email as validate_email_lib, EmailNotValidError


def validate_email(email):
    """Validate email address"""
    try:
        validate_email_lib(email)
        return True
    except EmailNotValidError:
        return False


def validate_password(password):
    """
    Validate password strength
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if len(password) < 8:
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'\d', password):
        return False

    return True


def validate_username(username):
    """
    Validate username
    Requirements:
    - 3-30 characters
    - Alphanumeric and underscore only
    """
    if not (3 <= len(username) <= 30):
        return False

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False

    return True


def validate_phone(phone):
    """Validate phone number"""
    # Simple validation - can be customized based on requirements
    phone_digits = re.sub(r'\D', '', phone)
    return 10 <= len(phone_digits) <= 15


def validate_url(url):
    """Validate URL"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

