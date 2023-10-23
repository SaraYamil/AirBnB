#!/usr/bin/python3
"""
Test for BaseModel class
"""

import unittest
from datetime import datetime
from uuid import UUID
import json
import os
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class test_basemodel(unittest.TestCase):
    """
    Test for BaseModel class
    """

    @classmethod
    def set_up(test_cls):
        """
        Set up test class
        """
        try:
            os.rename("file.json", "tmp_file")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        test_cls.storage = FileStorage()
        test_cls.base = BaseModel()

    @classmethod
    def tear_down(test_cls):
        """
        Tear down test class
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp_file", "file.json")
        except IOError:
            pass
        del test_cls.storage
        del test_cls.base

    def set_two_mdls(self):
        """
        Set up two models

        Returns:
            tuple: two BaseModel instances
        """
        base = BaseModel()
        self.assertNotEqual(self.base.id, base.id)
        self.assertLess(self.base.created_at, base.created_at)
        self.assertLess(self.base.updated_at, base.updated_at)

    def test_to_dict(self):
        """
        Test to_dict method
        """
        nw_base = self.base.to_dict()
        self.assertEqual(dict, type(nw_base))
        self.assertEqual(self.base.id, nw_base["id"])
        self.assertEqual("BaseModel", nw_base["__class__"])
        self.assertEqual(self.base.created_at.isoformat(),
                         nw_base["created_at"])
        self.assertEqual(self.base.updated_at.isoformat(),
                         nw_base["updated_at"])
        self.assertEqual(nw_base.get("_sa_instance_state", None), None)

    @unittest.skipIf(os.getenv("HBNB_ENV") is not None, "Testing DBStorage")
    def test_save(self):
        new_bs = self.base.updated_at
        self.base.save()
        self.assertLess(new_bs, self.base.updated_at)
        with open("file.json", "r") as file:
            self.assertIn("BaseModel.{}".format(self.base.id), file.read())

    def test_meth(self):
        self.assertTrue(hasattr(BaseModel, "__init__"))
        self.assertTrue(hasattr(BaseModel, "save"))
        self.assertTrue(hasattr(BaseModel, "to_dict"))
        self.assertTrue(hasattr(BaseModel, "__str__"))
        self.assertTrue(hasattr(BaseModel, "delete"))

    def str_attrs(self):
        self.assertEqual(datetime, type(self.base.created_at))
        self.assertEqual(datetime, type(self.base.updated_at))
        self.assertEqual(str, type(self.base.id))


if __name__ == "__main__":
    unittest.main()
