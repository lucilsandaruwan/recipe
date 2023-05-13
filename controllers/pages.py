from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.auth import AuthService
from utils.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user
from models.recipe_category import RecipeCategory
from models.recipe import Recipe
from models.user import User
from database import or_, and_

pages_bp = Blueprint('pages', __name__,)

# home page handler
@pages_bp.route('/', methods=['GET'])
def home():
    cards_limit = 6
    ja_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(cards_limit).all()
    h_recipes = Recipe.query.join(RecipeCategory).filter(RecipeCategory.title == "Healthy")\
    .order_by(Recipe.created_at.desc()).limit(cards_limit).all()

    v_recipes = Recipe.query.join(RecipeCategory).filter(RecipeCategory.title == "Vegitarian")\
    .order_by(Recipe.created_at.desc()).limit(cards_limit).all()

    b_recipes = Recipe.query.join(RecipeCategory).filter(RecipeCategory.title == "Baking")\
    .order_by(Recipe.created_at.desc()).limit(cards_limit).all()
    page_js = [
        'scripts/slider.js'
    ]
    categories = RecipeCategory.query.all()
    return render_template(
        'pages/home.html'
        , ja_recipes=ja_recipes
        , categories=categories
        , h_recipes=h_recipes
        , v_recipes = v_recipes
        , b_recipes = b_recipes
        , page_js = page_js
    )

@pages_bp.route('/search', methods=['GET'])
def search():
    per_page = 1

    search_query = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    query = Recipe.query.join(RecipeCategory).join(User).filter(
        or_(
            RecipeCategory.title.ilike(f'%{search_query}%')
            ,Recipe.title.ilike(f'%{search_query}%')
            ,User.name.ilike(f'%{search_query}%')
        )
    ).order_by(Recipe.created_at.desc())

    recipes = query.paginate(page=page, per_page=per_page)
    total_count = recipes.total
    next = recipes.next_num if recipes.has_next else None
    prev = recipes.prev_num if recipes.has_prev else None

    # Calculate the range of records being displayed
    start_index = (page - 1) * per_page + 1
    end_index = min(start_index + per_page - 1, total_count)
    showing = f"{start_index} - {end_index} of {total_count} recipes for \"{search_query}\""""

    return render_template(
        'pages/search_results.html'
        , search_results=recipes.items
        , showing=showing
        , next = next
        , prev = prev
        , q = search_query
    )

