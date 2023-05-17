import datetime
from database import db, Model, session, Column, Integer, String, ForeignKey, Text
from flask_login import UserMixin

class Methods(Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    discription = Column(Text)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=False)
    
    def save(self):
        session.add(self)
        session.commit()
    