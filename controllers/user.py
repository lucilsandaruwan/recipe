from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.auth import AuthService
from utils.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user
from utils.decorators import redirect_if_authenticated

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register', methods=['GET', 'POST'])
@redirect_if_authenticated
def profile():