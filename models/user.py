from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from web_flask import login
from models.base_model import Base, BaseModel
from models.data import Data
from uuid import uuid4


class User(Base, BaseModel, UserMixin):
    """User class"""
    __tablename__ = 'users'
    username = Column(String(128), nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    email = Column(String(128), nullable=False, index=True)
    
    data = relationship('Data', back_populates='user')

    def __init__(self, username, password, email, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid4())
        self.username = username
        self.set_password(password)
        self.email = email

    def set_password(self, password):
        """Sets password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks password"""
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    from models import db_storage
    users = db_storage.all(User)
    for user in users.values():
        if user.id == id:
            return user
