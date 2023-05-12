from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user

def redirect_if_authenticated(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already logged in', 'info')
            return redirect(url_for('home.home'))
        return func(*args, **kwargs)
    return decorated_view
