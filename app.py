from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from services.auth import AuthService
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
app.config['SECRET_KEY'] = 'recipe_123'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Tell Flask-Login where to locate the user loader function
@login_manager.user_loader
def load_user(user_id):
    from services.auth import AuthService
    return AuthService().get_user_by_id(user_id)

from controllers.auth import auth_bp as auth_blueprint
app.register_blueprint(auth_blueprint)

from controllers.pages import pages_bp as pages_blueprint
app.register_blueprint(pages_blueprint)



# Import the models module to ensure the table is created
from models.recipe import Recipe
from models.ingredients import Ingredients
from models.methods import Methods
from models.user import User
from models.recipe_category import RecipeCategory

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)


