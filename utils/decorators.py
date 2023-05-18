from functools import wraps
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from flask_login import current_user

def guest_users_only(func):
    """
    A decorator to ensure that the user is a guest (i.e., not logged in) before allowing access
    to a particular view. If the user is logged in, they will be redirected to the home page with
    a flash message indicating that they are already logged in.

    Usage: add the decorator `@guest_users_only` to the view function that should only be accessible
    to guest users.

    Args:
        func: the view function to be decorated

    Returns:
        decorated_view: the decorated view function
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already logged in', 'error')
            return redirect(url_for('pages.home'))
        return func(*args, **kwargs)

    return decorated_view

