'''
This file is created extending the SQLAlchemy Model to create User related functions 
'''
import datetime
from database import db, Model, session, Column, Boolean, Integer, String, DateTime, relationship
from flask_login import UserMixin

class User(Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(20))
    is_active = Column(Boolean, default=True)
    user_type = Column(String(20), default="user")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    recipe = relationship('Recipe', backref='user', lazy=True)
    
    def save(self):
        ''' Register new user'''
        session.add(self)
        session.commit()
    
    
    def get_id(self):
        ''' get user Id'''
        return self.id