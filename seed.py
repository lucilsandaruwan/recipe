''' This file is to add initial data as seeds
    Basically this should be run before start the application
    command: python seed.py
'''
from app import app, db
from models.recipe_category import RecipeCategory
from models.user import User
from models.ingredients import Ingredients
from models.methods import Methods
from models.recipe import Recipe
with app.app_context():
    ''' add all seed command to insert data to tables '''
    db.create_all()

    # recipe table inital data
    print("recipes category insert")
    h_recipe = RecipeCategory(
        title='Healthy'
        , slogan='Fresh ingredients, vibrant colors, and balanced flavors create healthy recipes.'
        , image="images/site/healthy.jpg"
    )
    if not RecipeCategory.query.filter_by(title=h_recipe.title).first():
        db.session.add(h_recipe)
        db.session.commit()
    else: 
        h_recipe = RecipeCategory.query.filter_by(title=h_recipe.title).first()
    v_recipe = RecipeCategory(
        title = 'Vegitarian'
        , slogan='Meatless meals, packed with flavor and nutrients, celebrate vegetables.'
        , image="images/site/vegitarian.jpg"
    )
    if not RecipeCategory.query.filter_by(title=v_recipe.title).first():
        db.session.add(v_recipe)
        db.session.commit()
    else: 
        v_recipe = RecipeCategory.query.filter_by(title=v_recipe.title).first()
    b_recipe = RecipeCategory(
        title='Baking'
        , slogan='Baking recipes combine science and creativity for delicious treats.'
        , image="images/site/baking.jpg"
    )
    if not RecipeCategory.query.filter_by(title=b_recipe.title).first():
        db.session.add(b_recipe)
        db.session.commit()
    else: 
        b_recipe = RecipeCategory.query.filter_by(title=b_recipe.title).first()

    o_recipe = RecipeCategory(
        title='Other'
        , slogan='Delicious and diverse dishes that range from simple to complex, inspired by global cuisines and seasonal ingredients.'
        , image="images/site/other.jpeg"
    )
    if not RecipeCategory.query.filter_by(title=o_recipe.title).first():
        db.session.add(o_recipe)
        db.session.commit()
    else: 
        o_recipe = RecipeCategory.query.filter_by(title=o_recipe.title).first()
    print("recipes category insert completed")

    print("first user insert")
    admin_user = User(
        name = "James Martin"
        ,email = "admin@recipe.com"
        ,password = "mock_password_does_not_work"
        ,user_type = "admin"
    )

    if not User.query.filter_by(email=admin_user.email).first():
        db.session.add(admin_user)
        db.session.commit()
    else: 
        admin_user = User.query.filter_by(email=admin_user.email).first()
    print("first user insert completed")
    
    print(" recipe insert")
    recipe1 = Recipe(
        title = 'Four-Cheese Stuffed Shells'
        ,description = "Indulge in the cheesy goodness of saucy jumbo pasta shells stuffed with four kinds of cheese: ricotta, Asiago, mozzarella, and cottage cheese. Prepare the dish ahead of time and follow the recipe instructions to freeze it for a delicious, ready-to-bake meal."
        ,image = "stuffed_shells.jpeg"
        ,recipe_category_id = v_recipe.id 
        ,user_id = admin_user.id # for the first user
    )
    if not Recipe.query.filter_by(image=recipe1.image).first():
        db.session.add(recipe1)
        db.session.commit()
    else:
        recipe1 = Recipe.query.filter_by(image=recipe1.image).first()
    
    recipe2 = Recipe(
        title = 'Vietnamese chicken pho'
        ,description = "Indulge in the cheesy goodness of saucy jumbo pasta shells stuffed with four kinds of cheese: ricotta, Asiago, mozzareSavory, low-fat, high-protein broth, with fresh herbs, lean meats, and rice noodles, make pho a nutritious and satisfying meal."
        ,image = "pho.jpg"
        ,recipe_category_id = h_recipe.id 
        ,user_id = admin_user.id # for the first user
    )
    if not Recipe.query.filter_by(image=recipe2.image).first():
        db.session.add(recipe2)
        db.session.commit()
    else:
        recipe2 = Recipe.query.filter_by(image=recipe2.image).first()
    
    recipe3 = Recipe(
        title = 'Lemon and poppy seed scones'
        ,description = "These easy lemon and poppy seed scones are gluten and dairy-free! Decorate with citrus-infused icing sugar and lemon zest for a bake that's sure to impress."
        ,image = "baking.jpg"
        ,recipe_category_id = b_recipe.id 
        ,user_id = admin_user.id # for the first user
    )
    if not Recipe.query.filter_by(image=recipe3.image).first():
        db.session.add(recipe3)
        db.session.commit()
    else:
        recipe3 = Recipe.query.filter_by(image=recipe3.image).first()
    
    recipe4 = Recipe(
        title = 'Cosmopolitan'
        ,description = "A well-known fruity favourite that kickstarted the cocktail renaissance in the 90s. This classic throwback is sure to impress your guests, shake up your vodka, orange liqueur, lime and cranberry juice, pour it up and garnish with an orange twist."
        ,image = "drink.jpg"
        ,recipe_category_id = o_recipe.id 
        ,user_id = admin_user.id 
    )
    if not Recipe.query.filter_by(image=recipe4.image).first():
        db.session.add(recipe4)
        db.session.commit()
    else:
        recipe4 = Recipe.query.filter_by(image=recipe4.image).first()
    
    print("recipe insert completed")

    print("ingradients insert")
    if not Ingredients.query.filter_by(recipe_id=recipe1.id).first():
        ingredients = [
            Ingredients(
                name = "Uncooked jumbo pasta shells"
                ,quantity = 6
                ,unit = ""
                ,recipe_id = recipe1.id
            ),
            Ingredients(
                name = "Shredded part-skim mozzarella cheese, divided"
                ,quantity = "1/2"
                ,unit = "Cups"
                ,recipe_id = recipe1.id
            ),
            Ingredients(
                name = "Shredded Asiago cheese"
                ,quantity = "1/4"
                ,unit = "Cups"
                ,recipe_id = recipe1.id
            ),
            Ingredients(
                name = "Cup ricotta cheese"
                ,quantity = "1/4"
                ,unit = "Cups"
                ,recipe_id = recipe1.id
            )
        ]
        db.session.add_all(ingredients)
        db.session.commit()

    if not Ingredients.query.filter_by(recipe_id=recipe2.id).first():
        ingredients = [
            Ingredients(
                name = "Noodles"
                ,quantity = 250
                ,unit = "g"
                ,recipe_id = recipe2.id
            ),
            Ingredients(
                name = "Pork meat balls"
                ,quantity = "100"
                ,unit = "g"
                ,recipe_id = recipe2.id
            ),
            Ingredients(
                name = "Water"
                ,quantity = "2"
                ,unit = "Cups"
                ,recipe_id = recipe2.id
            ),
            Ingredients(
                name = "Mixed vegitables"
                ,quantity = "250"
                ,unit = "g"
                ,recipe_id = recipe2.id
            )
        ]
        db.session.add_all(ingredients)
        db.session.commit()
    
    if not Ingredients.query.filter_by(recipe_id=recipe4.id).first():
        ingredients = [
            Ingredients(
                name = "Vodka"
                ,quantity = 80
                ,unit = "ml"
                ,recipe_id = recipe4.id
            ),
            Ingredients(
                name = "Cointreau or triple sec"
                ,quantity = "40"
                ,unit = "ml"
                ,recipe_id = recipe4.id
            ),
            Ingredients(
                name = "lime juice (about 1 large lime)"
                ,quantity = "20"
                ,unit = "ml"
                ,recipe_id = recipe4.id
            ),
            Ingredients(
                name = "cranberry juice drink"
                ,quantity = "60"
                ,unit = "ml"
                ,recipe_id = recipe4.id
            )

        ]
        db.session.add_all(ingredients)
        db.session.commit()

    if not Ingredients.query.filter_by(recipe_id=recipe3.id).first():
        ingredients = [
            Ingredients(
                name = "Wheet Flour"
                ,quantity = 1
                ,unit = "Cup"
                ,recipe_id = recipe3.id
            ),
            Ingredients(
                name = "Water"
                ,quantity = "1"
                ,unit = "Cup"
                ,recipe_id = recipe3.id
            ),
            Ingredients(
                name = "Sugar"
                ,quantity = "1"
                ,unit = "spoon"
                ,recipe_id = recipe3.id
            )
        ]
        db.session.add_all(ingredients)
        db.session.commit()
    print("ingradients insert end")

    print("Methods insert")
    if not Methods.query.filter_by(recipe_id=recipe1.id).first():
        methods = [
            Methods(
                title = "Dummy text of the printing and typesetting"
                ,discription = "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make"
                ,recipe_id = recipe1.id
            ),
            Methods(
                title = "Contrary to popular belief, "
                ,discription = "Lorem Ipsum is not simply random text. It has roots in a piece of"
                ,recipe_id = recipe1.id
            )
        ]
        db.session.add_all(methods)
        db.session.commit()

    if not Methods.query.filter_by(recipe_id=recipe2.id).first():
        methods = [
            Methods(
                title = "Dummy text of the printing and typesetting"
                ,discription = "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make"
                ,recipe_id = recipe2.id
            ),
            Methods(
                title = "Contrary to popular belief, "
                ,discription = "Lorem Ipsum is not simply random text. It has roots in a piece of"
                ,recipe_id = recipe2.id
            )
        ]
        db.session.add_all(methods)
        db.session.commit()
    
    if not Methods.query.filter_by(recipe_id=recipe4.id).first():
        methods = [
            Methods(
                title = "Dummy text of the printing and typesetting"
                ,discription = "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make"
                ,recipe_id = recipe4.id
            ),
            Methods(
                title = "Contrary to popular belief, "
                ,discription = "Lorem Ipsum is not simply random text. It has roots in a piece of"
                ,recipe_id = recipe4.id
            )
        ]
        db.session.add_all(methods)
        db.session.commit()
    
    if not Methods.query.filter_by(recipe_id=recipe3.id).first():
        methods = [
            Methods(
                title = ""
                ,discription = "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make"
                ,recipe_id = recipe3.id
            ),
            Methods(
                title = ""
                ,discription = "Lorem Ipsum is not simply random text. It has roots in a piece of"
                ,recipe_id = recipe3.id
            )
        ]
        db.session.add_all(methods)
        db.session.commit()
    print("ingradients insert end")

