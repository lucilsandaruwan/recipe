import datetime
from database import db, Model, session, Column, Integer, String, DateTime, relationship
from flask_login import UserMixin

class RecipeCategory(Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    slogan = Column(String(50))
    image = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    recipe = relationship('Recipe', backref='recip_category', lazy=True)

    def save(self):
        session.add(self)
        session.commit()
    
    def get_id(self):
        return self.id