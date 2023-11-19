"""User class for Data_Visualizer"""

from sqlalchemy import Column, String

class User():
    """user class"""
    __tablename__ = 'users'
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)

    def __init__(self, username, password, email):
        """initializes user"""
        self.username = username
        self.password = password
        self.email = email