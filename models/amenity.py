#!/usr/bin/python3
"""
Amennity class
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """
    Amenity class

    Attributes:
        name (str): name of the amenity
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   viewonly=False)
