#!/usr/bin/python3
"""
City class
"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """
    City class for AirBnB clone project

    Attributes:
        name (str): name of city
        state_id (str): state id
    """

    __tablename__ = "cities"
    name = (
        Column(String(128), nullable=False)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )
    state_id = (
        Column(String(60), ForeignKey("states.id"), nullable=False)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )
    places = (
        relationship("Place", cascade="all, delete, delete-orphan",
                     backref="cities")
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else None
    )
