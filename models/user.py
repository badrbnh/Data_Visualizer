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


@login.user_loader
def load_user(id):
    from models import db_storage
    users = db_storage.all(User)
    for user in users.values():
        if user.id == id:
            return user

