#!/usr/bin/python3
"""
Test for City class
"""

import os
from datetime import datetime
from models.state import State
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
import pep8
import models
import MySQLdb
import unittest
from sqlalchemy.orm import sessionmaker


class test_City(test_basemodel):
    """
    Test for City class
    """

    @classmethod
    def set_up(cls):
        """
            City tests
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)

        if type(models.db_storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            sess = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = sess()

    @classmethod
    def tear_down(cls):
        """
            City tests
        """
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

    def test_string(self):
        """
        Test string representation
        """
        strin = self.city.__str__()
        self.assertIn("[City] ({})".format(self.city.id), strin)
        self.assertIn("'id': '{}'".format(self.city.id), strin)
        self.assertIn("'created_at': {}".format(
            repr(self.city.created_at)), strin)
        self.assertIn("'updated_at': {}".format(
            repr(self.city.updated_at)), strin)
        self.assertIn("'name': '{}'".format(self.city.name), strin)
        self.assertIn("'state_id': '{}'".format(self.city.state_id), strin)

    @unittest.skipIf(type(models.db_storage) == DBStorage,
                     "Testing DBStorage")
    def test_save_filestorage(self):
        """
        Test save method with FileStorage
        """
        old_db = self.city.updated_at
        self.city.save()
        self.assertLess(old_db, self.city.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("City." + self.city.id, f.read())

    @unittest.skipIf(type(models.db_storage) == FileStorage,
                     "Testing FileStorage")
    def test_storage(self):
        """
        Test save method with DBStorage
        """
        old_s = self.city.updated_at
        self.state.save()
        self.city.save()
        self.assertLess(old_s, self.city.updated_at)
        database = MySQLdb.connect(user="hbnb_test",
                                   passwd="hbnb_test_pwd",
                                   db="hbnb_test_db")
        curs = database.cursor()
        curs.execute("SELECT * \
                      FROM `cities` \
                      WHERE BINARY name = '{}'".format(self.city.name))
        quer = curs.fetchall()
        self.assertEqual(1, len(quer))
        self.assertEqual(self.city.id, quer[0][0])
        curs.close()

    def test_dict(self):
        """
        Test to_dict method
        """
        dict_city = self.city.to_dict()
        self.assertEqual(dict, type(dict_city))
        self.assertEqual(self.city.id, dict_city["id"])
        self.assertEqual("City", dict_city["__class__"])
        self.assertEqual(self.city.created_at.isoformat(),
                         dict_city["created_at"])
        self.assertEqual(self.city.updated_at.isoformat(),
                         dict_city["updated_at"])
        self.assertEqual(self.city.name, dict_city["name"])
        self.assertEqual(self.city.state_id, dict_city["state_id"])

    def test_pep8(self):
        """
        Test pep8
        """
        pep_style = pep8.StyleGuide(quiet=True)
        pep = pep_style.check_files(["models/city.py"])
        self.assertEqual(pep.total_errors, 0, "fix pep8")

    def test_subclass(self):
        """
        Test is subclass
        """
        self.assertTrue(issubclass(City, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.city, City)

    def test_initialize(self):
        """
        Test initialization
        """
        city = City()
        self.assertNotEqual(self.city.id, city.id)
        self.assertLess(self.city.created_at, city.created_at)
        self.assertLess(self.city.updated_at, city.updated_at)

    def test_init_args_kwargs(self):
        """
        Test initialization with args and kwargs
        """
        date = datetime.utcnow()
        city = City("1", id="5", created_at=date.isoformat())
        self.assertEqual(city.id, "5")
        self.assertEqual(city.created_at, date)

    def test_attrs(self):
        """
        Test attrs
        """
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(City(
                state_id=self.state.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(City(name="San Jose"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()

    @unittest.skipIf(type(models.db_storage) == FileStorage,
                     "Testing FileStorage")
    def test_docstrings(self):
        """
        Test docstrings
        """
        self.assertIsNotNone(City.__doc__)

    def test_attributes(self):
        """
        Test attributes
        """
        city = City()
        self.assertEqual(str, type(city.id))
        self.assertEqual(datetime, type(city.created_at))
        self.assertEqual(datetime, type(city.updated_at))
        self.assertTrue(hasattr(city, "__tablename__"))
        self.assertTrue(hasattr(city, "name"))
        self.assertTrue(hasattr(city, "state_id"))

    @unittest.skipIf(type(models.db_storage) == FileStorage,
                     "Testing FileStorage")
    def test_state_relationship_deletes(self):
        """
        Test state relationship deletes
        """
        state = State(name="Georgia")
        self.dbstorage._DBStorage__session.add(state)
        self.dbstorage._DBStorage__session.commit()
        city = City(name="Atlanta", state_id=state.id)
        self.dbstorage._DBStorage__session.add(city)
        self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.delete(state)
        self.dbstorage._DBStorage__session.commit()
        database = MySQLdb.connect(user="hbnb_test",
                                   passwd="hbnb_test_pwd",
                                   db="hbnb_test_db")
        curs = database.cursor()
        curs.execute("SELECT * FROM cities WHERE BINARY name = 'Atlanta'")
        quer = curs.fetchall()
        curs.close()
        self.assertEqual(0, len(quer))


if __name__ == "__main__":
    unittest.main()
