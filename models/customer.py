"""module that defines the customer class"""

from models.user import User
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Customer(User):
    """class that inherits from user"""
    __tablename__ = 'customers'