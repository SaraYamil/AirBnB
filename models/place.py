#!/usr/bin/python3
"""
Place Module
"""

from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False,
    ),
)


class Place(BaseModel, Base):
    """
    Place class

    Attributes:
        __tablename__ (str): The name of the MySQL table to store Places
        city_id (sqlalchemy String): The Place's city ID
        user_id (sqlalchemy String): The Place's user ID
        name (sqlalchemy String): The Place's name
        description (sqlalchemy String): The Place's description
        number_rooms (sqlalchemy Integer): The Place's number of rooms
        number_bathrooms (sqlalchemy Integer): The Place's number of bathrooms
        max_guest (sqlalchemy Integer): The Place's maximum number of guests
        price_by_night (sqlalchemy Integer): The Place's price by night
        latitude (sqlalchemy Float): The Place's latitude
        longitude (sqlalchemy Float): The Place's longitude
        amenity_ids (list): A list of Amenity IDs

    Methods:
        __init__(self, *args, **kwargs): Initializes a Place instance
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review", cascade="all, delete, delete-orphan", backref="place"
        )

        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            back_populates="place_amenities",
        )
    else:
        @property
        def reviews(self):
            """
            Returns list of review instances with place_id equal to the
            current Place.id

            Returns:
                list: List of Review instances
            """
            variable = models.db_storage.all()
            alist = []
            output = []
            for key in variable:
                review = key.replace(".", " ")
                review = shlex.split(review)
                if review[0] == "Review":
                    alist.append(variable[key])
            for element in alist:
                if element.place_id == self.id:
                    output.append(element)
            return output

        @property
        def amenities(self):
            """
            Returns list of amenity instances based on the attribute
            amenity_ids
            """
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """
            Adds an Amenity.id to the attribute amenity_ids

            Args:
                obj (Amenity): Amenity instance to add to amenity_ids

            Returns:
                None
            """
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
