from sqlalchemy import Column, String
from models.user import User


class Admin(User):
    """Admin class"""
    __tablename__ = 'admins'

    def __init__(self, username, password, email, *args, **kwargs):
        """Initializes admin"""
        super().__init__(username=username, password=password, email=email, *args, **kwargs)