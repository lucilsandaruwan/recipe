from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.auth import AuthService
from utils.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user
from utils.decorators import guest_users_only

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
@guest_users_only
def register():
    form = RegistrationForm()
    page_css = [
        'css/forms.css'
    ]
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        AuthService.register_user(name, email, password)
        flash('Account created successfully', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, page_css = page_css)


@auth_bp.route('/login', methods=['GET', 'POST'])
@guest_users_only
def login():
    # guest_users_only()
    page_css = [
        'css/forms.css'
    ]
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = AuthService.get_user_by_email(email)

        if user and AuthService.verify_password(user, password):
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('pages.home'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('auth/login.html', form=form, page_css = page_css)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))


