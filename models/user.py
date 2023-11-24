from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from web_flask import login
import uuid
from models.base_model import Base, BaseModel

class User(Base, BaseModel, UserMixin):
    """User class"""
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True)
    username = Column(String(128), nullable=False)
    password_hash = Column(String(256), nullable=False)
    email = Column(String(128), nullable=False)

    def __init__(self, username, password, email, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        self.username = username
        self.set_password(password)
        self.email = email

    def set_password(self, password):
        """Sets password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks password"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_customer(self):
        """Checks if user is customer"""
        return isinstance(self, Customer)
    
    @property
    def is_admin(self):
        """Checks if user is admin"""
        return isinstance(self, Admin)

@login.user_loader
def load_user(id):
    """Loads the user"""
    from models import db_storage
    
    classes = [User, Customer, Admin]
    
    for cls in classes:
        users = db_storage.all(cls)
        for user in users.values():
            if user.id == id:
                return user

