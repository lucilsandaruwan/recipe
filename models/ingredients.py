import datetime
from database import db, Model, session, Column, Integer, String, ForeignKey
from flask_login import UserMixin

class Ingredients(Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    quantity = Column(String(50))
    unit = Column(String(20))
    recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=False)
    
    def save(self):
        session.add(self)
        session.commit()
    
    def get_id(self):
        return self.id