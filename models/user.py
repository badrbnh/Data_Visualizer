from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase
import uuid

class Base(DeclarativeBase):
    pass

class User(Base):
    """user class"""
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)

    def __init__(self, username, password, email):
        """initializes user"""
        self.id = str(uuid.uuid4())  # Ensure each user has a unique ID
        self.username = username
        self.password = password
        self.email = email

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
