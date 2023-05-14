from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User


class AuthService:
    @staticmethod
    def register_user(name, email, password):
        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password)
        user.save()

    @staticmethod
    def login_user(email, password):
        user = User.get_by_email(email)
        if user and check_password_hash(user.password, password):
            user.authenticated = True
            user.save()
            return user

    @staticmethod
    def logout_user():
        user = User.get_authenticated_user()
        if user:
            user.authenticated = False
            user.save()

    
    def get_user_by_id(self, user_id):
        # Query the database to get the user with the given id
        user = User.query.get(user_id)

        # Return the user object
        return user
    
    @staticmethod
    def get_user_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user
        
    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user.password, password)