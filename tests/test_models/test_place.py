#!/usr/bin/python3
"""
Test Place class
"""

from tests.test_models.test_base_model import test_basemodel
from models.place import Place


class test_Place(test_basemodel):
    """
    Test Place class
    """

    def __init__(self, *args, **kwargs):
        """
        Init method
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city(self):
        """
        Test city_id attribute
        """
        new_city = self.value()
        self.assertEqual(type(new_city.city_id), str)

    def test_price(self):
        """
        Test price_by_night attribute
        """
        new_inst = self.value()
        self.assertEqual(type(new_inst.price_by_night), int)

    def test_latitude(self):
        """
        Test latitude attribute
        """
        new_inst = self.value()
        self.assertEqual(type(new_inst.latitude), float)

    def test_longitude(self):
        """
        Test longitude attribute
        """
        new_inst = self.value()
        self.assertEqual(type(new_inst.latitude), float)

    def test_descr(self):
        """
        Test description attribute
        """
        new_descr = self.value()
        self.assertEqual(type(new_descr.description), str)

    def test_nums(self):
        """
        Test number_rooms attribute
        """
        new_num = self.value()
        self.assertEqual(type(new_num.number_rooms), int)

    def test_n_baths(self):
        """
        Test number_bathrooms attribute
        """
        new_num_baths = self.value()
        self.assertEqual(type(new_num_baths.number_bathrooms), int)

    def test_maximum_guests(self):
        """
        Test max_guest attribute
        """
        new_inst = self.value()
        self.assertEqual(type(new_inst.max_guest), int)

    def test_amenity(self):
        """
        Test amenity_ids attribute
        """
        new_inst = self.value()
        self.assertEqual(type(new_inst.amenity_ids), list)

    def test_user(self):
        """
        Test user_id attribute
        """
        new_user = self.value()
        self.assertEqual(type(new_user.user_id), str)

    def test_name(self):
        """
        Test name attribute
    """
        new_name = self.value()
        self.assertEqual(type(new_name.name), str)
