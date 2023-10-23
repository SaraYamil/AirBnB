#!/usr/bin/python3
"""
Review Module
"""

from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """
    Review class

    Attributes:
        __tablename__ (str): The name of the MySQL table to store Reviews
        place_id (sqlalchemy String): The Review's place ID
        user_id (sqlalchemy String): The Review's user ID
        text (sqlalchemy String): The Review's text

    Methods:
        __init__(self, *args, **kwargs): Initializes a Review instance
    """
    __tablename__ = 'reviews'
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    text = Column(String(1024), nullable=False)
