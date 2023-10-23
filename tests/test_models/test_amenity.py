#!/usr/bin/python3
"""
TestAmenity module
"""
from datetime import datetime
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
import os
import pep8
import models
import MySQLdb
import unittest
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestAmenity(unittest.TestCase):
    """
    Test the Amenity class

    Attributes:
        __engine: DBStorage or FileStorage object
        __session: DBStorage or FileStorage object
        __classes: list of class names of all the objects
    """

    @classmethod
    def set_up(cls):
        """
        Sets up unittest

        Creates a new Amenity instance

        Args:
            None
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.amenity = Amenity(name="The Andrew Lindburg treatment")

        if type(models.db_storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def destroy_class(cls):
        """
        Tears down unittest

        Deletes the test instances

        Args:
            None
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.amenity
        del cls.filestorage
        if type(models.db_storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_style(self):
        """
        Tests pep8

        Args:
            None
        """
        pep_style = pep8.StyleGuide(quiet=True)
        pep = pep_style.check_files(["models/amenity.py"])
        self.assertEqual(pep.total_errors, 0, "fix pep8")

    def test_docs(self):
        """Check for docstrings."""
        self.assertIsNotNone(Amenity.__doc__)

    def test_string(self):
        """
        Test for string representation

        Args:
            None
        """
        str = self.amenity.__str__()
        self.assertIn("[Amenity] ({})".format(self.amenity.id), str)
        self.assertIn("'id': '{}'".format(self.amenity.id), str)
        self.assertIn("'created_at': {}".format(
            repr(self.amenity.created_at)), str)
        self.assertIn("'updated_at': {}".format(
            repr(self.amenity.updated_at)), str)
        self.assertIn("'name': '{}'".format(self.amenity.name), str)

    @unittest.skipIf(type(models.db_storage) == DBStorage,
                     "Testing DBStorage")
    def test_storage(self):
        """
        Test for storage

        Args:
            None
        """
        old_storag = self.amenity.updated_at
        self.amenity.save()
        self.assertLess(old_storag, self.amenity.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Amenity." + self.amenity.id, f.read())

    @unittest.skipIf(type(models.db_storage) == FileStorage,
                     "Testing FileStorage")
    def test_save_dbstorage(self):
        """
        Test for save method
        """
        old_str = self.amenity.updated_at
        self.amenity.save()
        self.assertLess(old_str, self.amenity.updated_at)
        database_t = MySQLdb.connect(user="hbnb_test",
                                     passwd="hbnb_test_pwd",
                                     db="hbnb_test_db")
        curs = database_t.cursor()
        curs.execute("SELECT * \
                     FROM `amenities` \
                     WHERE BINARY name = '{}'".
                     format(self.amenity.name))
        quer = curs.fetchall()
        self.assertEqual(1, len(quer))
        self.assertEqual(self.amenity.id, quer[0][0])
        curs.close()

    def test_dictionary(self):
        """
        Test to_dict method

        Args:
            None
        """
        dict_amenity = self.amenity.to_dict()
        self.assertEqual(dict, type(dict_amenity))
        self.assertEqual(self.amenity.id, dict_amenity["id"])
        self.assertEqual("Amenity", dict_amenity["__class__"])
        self.assertEqual(self.amenity.created_at.isoformat(),
                         dict_amenity["created_at"])
        self.assertEqual(self.amenity.updated_at.isoformat(),
                         dict_amenity["updated_at"])
        self.assertEqual(self.amenity.name, dict_amenity["name"])

    def test_attrs(self):
        """
        Test for attributes

        Args:
            None
        """
        us = Amenity(email="a", password="a")
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertTrue(hasattr(us, "__tablename__"))
        self.assertTrue(hasattr(us, "name"))
        self.assertTrue(hasattr(us, "place_amenities"))

    @unittest.skipIf(type(models.db_storage) == FileStorage,
                     "Testing FileStorage")
    def test_email(self):
        """
        Test for email attribute

        Args:
            None
        """
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Amenity(password="a"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Amenity(email="a"))
            self.dbstorage._DBStorage__session.commit()

    def test_sub(self):
        """
        Test for subclass
        """
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_initialize(self):
        """
        Test for init
        """
        self.assertIsInstance(self.amenity, Amenity)

    def test_two_models(self):
        """
        Test for two objects

        Args:
            None
        """
        sess = Amenity(email="a", password="a")
        self.assertNotEqual(self.amenity.id, sess.id)
        self.assertLess(self.amenity.created_at, sess.created_at)
        self.assertLess(self.amenity.updated_at, sess.updated_at)

    def test_init_args_kwargs(self):
        """
        Test for instantation with args and kwargs

        Args:
            None
        """
        datat = datetime.utcnow()
        sett = Amenity("1", id="5", created_at=datat.isoformat())
        self.assertEqual(sett.id, "5")
        self.assertEqual(sett.created_at, datat)


if __name__ == "__main__":
    unittest.main()
