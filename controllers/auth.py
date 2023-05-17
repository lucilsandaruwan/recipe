from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.auth import AuthService
from utils.forms import RegistrationForm, LoginForm, UpdateProfileForm, ChangePasswordForm
from flask_login import login_user, logout_user, current_user, login_required
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
    elif form.errors.items():
        flash('Please correct the form errors and try again.', 'error')

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
            next = request.args.get('next')
            return redirect(next or url_for('pages.home'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('auth/login.html', form=form, page_css = page_css)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    c_user = current_user

    return render_template('auth/profile.html', user = c_user)

@auth_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm()
    user = current_user
    page_css = [
        'css/forms.css'
    ]
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        user = AuthService.update_profile(user, name, email)
        flash('Account Updated successfully', 'success')
        return redirect(url_for('auth.profile'))
    elif form.errors.items():
        flash('Please correct the form errors and try again.', 'error')
    else:
        form.init_prfile()
    return render_template('auth/update_profile.html', form = form, page_css = page_css)

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    user = current_user
    page_css = [
        'css/forms.css'
    ]
    if form.validate_on_submit():
        password = form.new_password.data
        user = AuthService.change_password(user, password)
        flash('Password changed successfully', 'success')
        return redirect(url_for('auth.profile'))
    elif form.errors.items():
        flash('Please correct the form errors and try again.', 'error')
    return render_template('auth/change_password.html', form = form, page_css = page_css)




