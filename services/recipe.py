from flask import current_app
from models.recipe_category import RecipeCategory
from models.recipe import Recipe
from models.user import User
from database import or_, and_
from werkzeug.utils import secure_filename
from datetime import datetime
from models.ingredients import Ingredients
from models.methods import Methods
import os

class RecipeService:
    # set the limit for the number of recipe cards displayed in a banner
    banners_card_limit = 6

    # Define the number of records to display per page in listing pages
    per_page = 1
    
    def get_latest_banner_recipes(self):
        # retrieve the latest recipes based on the created_at attribute
        return Recipe.query.order_by(Recipe.created_at.desc()).limit(self.banners_card_limit).all()
    
    def get_latest_banner_cat_recipes(self, category):
        # retrieve the latest recipes for a specific category
        return Recipe.query.join(RecipeCategory).filter(RecipeCategory.title == category)\
        .order_by(Recipe.created_at.desc()).limit(self.banners_card_limit).all()

    def get_all_categories(self):
        # retrieve all available recipe categories
        return RecipeCategory.query.all()
    
    def search_recipes(self, key, page):
        # Construct a database query to get the recipes in the specified category, sorted by creation date
        query = Recipe.query.join(RecipeCategory).join(User).filter(
            or_(
                RecipeCategory.title.ilike(f'%{key}%')
                ,Recipe.title.ilike(f'%{key}%')
                ,User.name.ilike(f'%{key}%')
            )
        ).order_by(Recipe.created_at.desc())

        # Use pagination to limit the number of records displayed and get metadata about the pagination state
        return query.paginate(page = page, per_page = self.per_page)
    
    def get_category_listing_recipes(self, category, page):
        # Construct a database query to get the recipes in the specified category, sorted by creation date
        query = Recipe.query.join(RecipeCategory).join(User).filter(
            RecipeCategory.title == category
        ).order_by(Recipe.created_at.desc())

        # Use pagination to limit the number of records displayed and get metadata about the pagination state
        return query.paginate(page = page, per_page = self.per_page)
    
    def get_user_created_recipes(self, user_id, page):
        # Construct a database query to get the recipes in the specified category, sorted by creation date
        query = Recipe.query.join(RecipeCategory).join(User).filter(
            User.id == user_id
        ).order_by(Recipe.created_at.desc())

        # Use pagination to limit the number of records displayed and get metadata about the pagination state
        return query.paginate(page = page, per_page = self.per_page)

    def get_category_for_select_field(self):
        return RecipeCategory.query.with_entities(RecipeCategory.id, RecipeCategory.title).all()

    def save_recipe_image(self, recipe_image, title):
        '''This function is to save uploaded image into the path and return the saved file name'''

        # Extract the file extension from the recipe_image filename
        extension = os.path.splitext(recipe_image.filename)[1].lower()

        # Create a unique and secure file name to save the file
        file_name = "{}_{}{}".format(datetime.now().strftime('%Y%m%d%H%M%S'), secure_filename(title), extension)

        # Upload directory path from app config and append the image file directory
        upload_path = current_app.config["UPLOAD_PATH"] + 'dishes/'

        # Create file path to save the image
        file_path = os.path.join(upload_path, file_name)

        # Save the image
        recipe_image.save(file_path)

        # Return the unique file name to save in the database
        return file_name
    
    def create_recipe(self, recipe_params, ingredients,  method_steps):
        '''
            this function is used to crate recipes with ingredients and methods
        '''
        # create recipe object
        recipe = Recipe(
            title = recipe_params['title']
            , description = recipe_params['description']
            ,image = recipe_params['file_name']
            ,recipe_category_id = recipe_params['category']
            ,user_id = recipe_params['user_id']
        )
        recipe.save()

        # loop through ingradients and save them
        for data in ingredients:
            print(data, 'data')
            ingradient = Ingredients(
                name = data['name']
                ,quantity = data['qty']
                ,unit = data['unit']
                ,recipe_id = recipe.id
            )
            ingradient.save()
        
        # loop through methods and save them
        for data in method_steps:
            method = Methods(
                title = data['title']
                , discription = data['discription']
                ,recipe_id = recipe.id
            )
            method.save()

        return recipe

    def get_recipe_bu_id(self, recipe_id):
        return Recipe.query.get(recipe_id)