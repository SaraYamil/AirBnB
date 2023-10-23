#!/usr/bin/python3
"""A unit test module for the console (command interpreter).
"""
import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """Represents the test class for the HBNBCommand class.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_create(self):
        """
        Tests the create command.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cns = HBNBCommand()
            cns.onecmd('create City name="Texas"')
            mid = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(mid), storage.all().keys())
            cns.onecmd('show City {}'.format(mid))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())
            clear_stream(cout)
            cns.onecmd('create User name="James" age=17 height=5.9')
            mid = cout.getvalue().strip()
            self.assertIn('User.{}'.format(mid), storage.all().keys())
            clear_stream(cout)
            cns.onecmd('show User {}'.format(mid))
            self.assertIn("'name': 'James'", cout.getvalue().strip())
            self.assertIn("'age': 17", cout.getvalue().strip())
            self.assertIn("'height': 5.9", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """
        Tests the show command.
        """
        with patch('sys.stdout', new=StringIO()) as output:
            cons = HBNBCommand()
            # showing a User instance
            instance = User(email="john25@gmail.com", password="123")
            database_connect = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            crs = database_connect.cursor()
            crs.execute('SELECT * FROM users WHERE \
                        id="{}"'.format(instance.id))
            output = crs.fetchone()
            self.assertTrue(output is None)
            cons.onecmd('show User {}'.format(instance.id))
            self.assertEqual(
                output.getvalue().strip(),
                '** no instance found **'
            )
            instance.save()
            database_connect = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            crs = database_connect.cursor()
            crs.execute('SELECT * FROM users WHERE \
                         id="{}"'.format(instance.id))
            clear_stream(output)
            cons.onecmd('show User {}'.format(instance.id))
            output = crs.fetchone()
            self.assertTrue(output is not None)
            self.assertIn('john25@gmail.com', output)
            self.assertIn('123', output)
            self.assertIn('john25@gmail.com', output.getvalue())
            self.assertIn('123', output.getvalue())
            crs.close()
            database_connect.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_count_db(self):
        """
        Tests the count command.
        """
        with patch('sys.stdout', new=StringIO()) as output:
            constructor = HBNBCommand()
            database_connect = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            crs = database_connect.cursor()
            crs.execute('SELECT COUNT(*) FROM states;')
            res = crs.fetchone()
            previous_output = int(res[0])
            constructor.onecmd('create State name="Enugu"')
            clear_stream(output)
            constructor.onecmd('count State')
            connt = output.getvalue().strip()
            self.assertEqual(int(connt), previous_output + 1)
            clear_stream(output)
            constructor.onecmd('count State')
            crs.close()
            database_connect.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """
        Tests the create command.
        """
        with patch('sys.stdout', new=StringIO()) as inst:
            constructor = HBNBCommand()
            # creating a model with non-null attribute(s)
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                constructor.onecmd('create User')
            # creating a User instance
            clear_stream(inst)
            constructor.onecmd('create User email="john25@gmail.com" \
                                password="123"')
            mid = inst.getvalue().strip()
            database_connect = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            crs = database_connect.cursor()
            crs.execute('SELECT * FROM users WHERE \
                        id="{}"'.format(mid))
            output = crs.fetchone()
            self.assertTrue(output is not None)
            self.assertIn('john25@gmail.com', output)
            self.assertIn('123', output)
            crs.close()
            database_connect.close()
