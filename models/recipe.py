import datetime
from database import db, Model, session, Column, Boolean, Integer, String, DateTime, ForeignKey, relationship, Text
from flask_login import UserMixin

class Recipe(Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(Text)
    image = Column(String(50), unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    ingredients = relationship('Ingredients', backref='recipe', lazy=True)
    methods = relationship('Methods', backref='recipe', lazy=True)
    recipe_category_id = Column(Integer, ForeignKey('recipe_category.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def save(self):
        session.add(self)
        session.commit()
    