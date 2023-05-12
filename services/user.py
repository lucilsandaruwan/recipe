from models.user import User
from database import db

class UserService:
    def register_user(self, username, email, password):
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
    
    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()