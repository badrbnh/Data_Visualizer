from sqlalchemy import Column, String
from models.user import User


class Customer(User):
    """Customer class"""
    __tablename__ = 'customers'

    def __init__(self, username, password, email, *args, **kwargs):
        """Initializes customer"""
        super().__init__(username=username, password=password, email=email, *args, **kwargs)