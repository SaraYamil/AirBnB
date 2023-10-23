#!/usr/bin/python3
"""
FileStorage class
"""

import json
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes
    JSON file to instances

    Attributes:
        __file_path (str): path to the JSON file
        __objects (dict): dictionary of objects
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary __objects

        Args:
            cls (str): name of the class

        Returns:
            dict: __objects
        """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            dictionary_obs = {}
            for key, data in self.__objects.items():
                if type(data) == cls:
                    dictionary_obs[key] = data
            return dictionary_obs
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id

        Args:
            obj (object): object to set in __objects

        Returns:
            None
        """
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)

        Returns:
            None
        """
        with open(FileStorage.__file_path, 'w') as f:
            temprary = {}
            temprary.update(FileStorage.__objects)
            for key, val in temprary.items():
                temprary[key] = val.to_dict()
            json.dump(temprary, f)

    def reload(self):
        """
        Deserializes the JSON file to objects

        Returns:
            None
        """
        all_classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temporary = {}
            with open(FileStorage.__file_path, 'r') as f:
                temporary = json.load(f)
                for key, data in temporary.items():
                    self.all()[key] = all_classes[data['__class__']](**data)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside

        Args:
            obj (object): object to delete

        Returns:
            None
        """
        if (obj):
            keyword = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[keyword]

    def close(self):
        """
        Calls reload method for deserializing the JSON file to objects
        """
        self.reload()
