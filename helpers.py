from functools import wraps
from flask import session, flash, redirect

# Helper function to convert to USD (you can modify this based on your requirements)
def usd(value):
    """Formats a number as a USD currency value"""
    return f"${value:,.2f}"

# Login required decorator
def login_required(f):
    """Decorator to ensure the user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("You must be logged in to access this page.", "danger")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
