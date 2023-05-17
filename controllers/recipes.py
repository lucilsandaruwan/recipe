from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.auth import AuthService
from services.recipe import RecipeService
from utils.forms import RecipeCreateForm, MethodForm, IngredientForm
from flask_login import login_user, logout_user, current_user, login_required
from utils.decorators import guest_users_only

recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@recipes_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    per_page = RecipeService.per_page
    page = request.args.get('page', 1, type=int)

    recipes = RecipeService().get_user_created_recipes(current_user.id, page)
    total_count = recipes.total
    next = recipes.next_num if recipes.has_next else None
    prev = recipes.prev_num if recipes.has_prev else None

    # Calculate the range of records being displayed
    start_index = (page - 1) * per_page + 1
    end_index = min(start_index + per_page - 1, total_count)
    showing = f"{start_index} - {end_index} of {total_count} recipes."

    return render_template(
        'recipes/user_recipes.html'
        , search_results=recipes.items
        , showing=showing
        , next = next
        , prev = prev
    )

@recipes_bp.route('/search', methods=['GET'])
def search():
    per_page = RecipeService.per_page
    search_query = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    recipes = RecipeService().search_recipes(search_query, page)
    total_count = recipes.total
    next = recipes.next_num if recipes.has_next else None
    prev = recipes.prev_num if recipes.has_prev else None

    # Calculate the range of records being displayed
    start_index = (page - 1) * per_page + 1
    end_index = min(start_index + per_page - 1, total_count)
    showing = f"{start_index} - {end_index} of {total_count} recipes for \"{search_query}\""
    
    return render_template(
        'recipes/search_results.html'
        , search_results=recipes.items
        , showing=showing
        , next = next
        , prev = prev
        , q = search_query
        ,current_user_id =  current_user.id if current_user.is_authenticated else None
    )

@recipes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = RecipeCreateForm()
    form.init_form()
    user = current_user
    page_css = [
        'css/forms.css'
    ]
    page_js = [
        '/scripts/recipes_forms.js'
    ]
    if form.validate_on_submit():
        recipe_service = RecipeService()
        title = form.title.data
        recipe_params = {
            'title': title,
            'file_name': form.recipe_image_name,
            'description': form.description.data,
            'category': form.category.data,
            'user_id': user.id
        }

        ingredients = []
        for ingredient in form.ingredients.entries:
            ingredient_form = ingredient.form
            if isinstance(ingredient_form, IngredientForm):
                ingredient_data = {
                    'name': ingredient_form.name.data,
                    'qty': ingredient_form.quantity.data,
                    'unit': ingredient_form.unit.data
                }
                ingredients.append(ingredient_data)

        method_steps = []
        for method in form.methods.entries:
            method_form = method.form
            if isinstance(method_form, MethodForm):
                method_data = {
                    'title': method_form.title.data
                    , 'discription': method_form.discription.data
                }
                method_steps.append(method_data)
            
        

        new_recipe = recipe_service.create_recipe(recipe_params, ingredients,  method_steps)
        flash('Account Updated successfully', 'success')
        return redirect(url_for('recipes.index'))

    elif form.errors.items():
        flash('Please correct the form errors and try again.', 'error')
    return render_template('recipes/create_recipe.html', form = form, page_css = page_css, page_js = page_js)

@recipes_bp.route('/<int:recipe_id>')
def get_recipe(recipe_id):
    # Endpoint function to load recipe details page

    recipe = RecipeService().get_recipe_bu_id(recipe_id)
    page_css = [
        'css/recipe_details.css'
    ]
    return render_template('recipes/details.html', recipe=recipe, page_css = page_css)
    