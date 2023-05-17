"""
This file defines the routes for the Flask application. It contains handlers for rendering HTML templates and handling user requests.

Functions:
    home(): Renders the home page of the website.
    search(): Renders the search results page based on the user's query.
    healthy(): Renders the listing page for the "Healthy" recipe category.
    vegetarian(): Renders the listing page for the "Vegetarian" recipe category.
    baking(): Renders the listing page for the "Baking" recipe category.
    miscellaneous(): Renders the listing page for the "Miscellaneous" recipe category.
    category_listing(category, showing): Renders the listing page for a given recipe category.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.auth import AuthService
from utils.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user
from models.recipe_category import RecipeCategory
from models.recipe import Recipe
from services.recipe import RecipeService
from models.user import User
from database import or_, and_

pages_bp = Blueprint('pages', __name__,)


@pages_bp.route('/', methods=['GET'])
def home():
    r_service = RecipeService()
    ja_recipes = r_service.get_latest_banner_recipes()
    categories = ["Healthy", "Vegitarian", "Baking"]
    cat_reipes = list(map(lambda c: r_service.get_latest_banner_cat_recipes(c), categories))
    page_js = [
        'scripts/slider.js'
    ]
    categories = r_service.get_all_categories()
    return render_template(
        'pages/home.html'
        , ja_recipes=ja_recipes
        , categories=categories
        , h_recipes=cat_reipes[0]
        , v_recipes = cat_reipes[1]
        , b_recipes = cat_reipes[2]
        , page_js = page_js
    )


@pages_bp.route('/healthy', methods=['GET'])
def healthy():
    showing = '''Explore a wide range of nutritious and delicious healthy recipes with our pagination feature. 
                Start with the first {}-{} out of {} recipes and browse at your leisure.'''
    category = "Healthy"
    return category_listing(category, showing)

@pages_bp.route('/vegitarian', methods=['GET'])
def vegitarian():
    showing = '''Explore a wide range of delicious and healthy vegetarian recipes with our pagination feature. 
                Start with the first {}-{} out of {} recipes and discover new flavors at your leisure.'''
    category = "Vegitarian"
    return category_listing(category, showing)

@pages_bp.route('/baking', methods=['GET'])
def baking():
    showing = '''Indulge your sweet tooth with our collection of delicious and easy-to-follow baking recipes. 
                Start with the first {}-{} out of {} recipes and bake up a storm at your own pace.'''
    category = "Baking"
    return category_listing(category, showing)

@pages_bp.route('/miscellaneous', methods=['GET'])
def miscellaneous():
    showing = '''Explore a diverse selection of mouth-watering recipes from our miscellaneous category. 
    Start with the first {}-{} out of {} recipes and discover new favorites at your own pace.'''
    category = "Miscellaneous"
    return category_listing(category, showing)

def category_listing(category, showing):
    
    per_page = RecipeService.per_page
    # Get the current page number from the URL parameter or default to the first page
    page = request.args.get('page', 1, type=int)
    
    recipes =  RecipeService().get_category_listing_recipes(category, page)
    total_count = recipes.total
    next = recipes.next_num if recipes.has_next else None
    prev = recipes.prev_num if recipes.has_prev else None

    # Calculate the range of records being displayed
    start_index = (page - 1) * per_page + 1
    end_index = min(start_index + per_page - 1, total_count)

    # Replace any placeholders in the 'showing' message with the actual values
    showing = showing.format(start_index, end_index, total_count)

    # Render the category listing HTML template and pass in the search results, pagination metadata, and category title
    return render_template(
        'pages/category_listing.html',
        search_results=recipes.items,
        showing=showing,
        next=next,
        prev=prev,
        title=category
    )
