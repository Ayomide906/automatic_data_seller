# utils/general_utils.py
import re
from datetime import datetime, timedelta
from models.database_models import SessionLocal


def extract_phone_number(text):
    """Extract phone number from text"""
    # Nigerian phone number patterns
    patterns = [
        r'(\d{11})',  # 11-digit numbers
        r'(\d{10})',  # 10-digit numbers
        r'(\+234\d{10})',  # International format
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]

    return None


def format_currency(amount):
    """Format amount as Nigerian Naira"""
    return f"₦{amount:,.2f}"


def is_recent_transaction(transaction_date, hours=24):
    """Check if transaction is within specified hours"""
    if not transaction_date:
        return False

    time_difference = datetime.now() - transaction_date
    return time_difference < timedelta(hours=hours)


def get_db_session():
    """Get database session"""
    return SessionLocal()


def close_db_session(session):
    """Close database session"""
    session.close()