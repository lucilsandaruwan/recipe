from models.recipe_category import RecipeCategory
from models.recipe import Recipe
from models.user import User
from database import or_, and_

class RecipeService:
    # set the limit for the number of recipe cards displayed in a banner
    banners_card_limit = 6

    # Define the number of records to display per page in listing pages
    per_page = 10
    
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