from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from web_flask import login
from models.base_model import Base, BaseModel
from models.data import Data
from models.img import Img

from uuid import uuid4

class User(Base, BaseModel, UserMixin):
    """User class"""
    __tablename__ = 'users'
    username = Column(String(128), nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    email = Column(String(128), nullable=False, index=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_token = Column(String(128))
    
    data = relationship('Data', back_populates='user')
    img = relationship('Img', back_populates='user')

    def __init__(self, username, password, email, is_verified=False, verification_token=None, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid4())
        self.username = username
        self.set_password(password)
        self.email = email
        self.is_verified = is_verified
        self.verification_token = verification_token

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
