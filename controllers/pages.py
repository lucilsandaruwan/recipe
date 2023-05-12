from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.auth import AuthService
from utils.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user
from models.recipe_category import RecipeCategory
from models.recipe import Recipe

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
    ja_recipes = []
    for i in range(3):
       ja_recipes.append(
           {
                "title": "Test title1" + str(i)
                ,"img": "https://realfood.tesco.com/media/images/1400x919-Mexican-inspired-black-bean-bake-d8a3f379-2d52-42e5-9ed6-46e79f920499-0-1400x919.jpg"
            }
       ) 
    return render_template('pages/home.html', ja_recipes=ja_recipes)

