#!/usr/bin/python3
"""
User Module
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """
    User class

    Attributes:
        __tablename__ (str): The name of the MySQL table to store Users
        email (sqlalchemy String): The user's email address
        password (sqlalchemy String): The user's password
        first_name (sqlalchemy String): The user's first name
        last_name (sqlalchemy String): The user's last name
        places (sqlalchemy relationship): The User-Place relationship
        reviews (sqlalchemy relationship): The User-Review relationship

    Methods:
        __init__(self, *args, **kwargs): Initializes a User instance
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", backref="user", cascade="delete")
    reviews = relationship("Review", backref="user", cascade="delete")
