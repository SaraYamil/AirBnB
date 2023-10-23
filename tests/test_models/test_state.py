#!/usr/bin/python3
"""
Test State class
"""

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import models
import MySQLdb
from models.city import City
from models.state import State
import os
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import unittest
from datetime import datetime
from models.base_model import Base, BaseModel


class TestState(unittest.TestCase):
    """
    Test State class
    """

    @classmethod
    def set_up(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.state = State(name="California")
        cls.city = City(name="San Jose", state_id=cls.state.id)

        if type(models.db_storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tear_down(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.state
        del cls.city
        del cls.filestorage
        if type(models.db_storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_init(self):
        self.assertIsInstance(self.state, State)

    def test_two_models_are_unique(self):
        st = State()
        self.assertNotEqual(self.state.id, st.id)
        self.assertLess(self.state.created_at, st.created_at)
        self.assertLess(self.state.updated_at, st.updated_at)

    def test_init_args_kwargs(self):
        dt = datetime.utcnow()
        st = State("1", id="5", created_at=dt.isoformat())
        self.assertEqual(st.id, "5")
        self.assertEqual(st.created_at, dt)

    def test_attributes(self):
        st = State()
        self.assertEqual(str, type(st.id))
        self.assertEqual(datetime, type(st.created_at))
        self.assertEqual(datetime, type(st.updated_at))
        self.assertTrue(hasattr(st, "name"))

    @unittest.skipIf(type(models.db_storage) == FileStorage,
                     "Testing FileStorage")
    def test_nullable_attributes(self):
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(State())
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()

    @unittest.skipIf(type(models.db_storage) == DBStorage,
                     "Testing DBStorage")
    def test_cities(self):
        key = "{}.{}".format(type(self.city).__name__, self.city.id)
        self.filestorage._FileStorage__objects[key] = self.city
        cities = self.state.cities
        self.assertTrue(list, type(cities))
        self.assertIn(self.city, cities)


if __name__ == "__main__":
    unittest.main()
