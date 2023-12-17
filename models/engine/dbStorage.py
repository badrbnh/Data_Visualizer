#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.user import User
from models.data import Data
from models.img import Img
from models.base_model import Base
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
classes = {"User": User, "Data": Data, "Img": Img}

class DBStorage():
    """this class stores stores data to database"""
    """interacts with the MySQL database"""
    __engine = None
    __session = None
    load_dotenv()
    def __init__(self, app=None):
        """Instantiate a DBStorage object"""
        DV_MYSQL_USER = getenv('DV_MYSQL_USER')
        DV_MYSQL_PWD = getenv('DV_MYSQL_PWD')
        DV_MYSQL_HOST = getenv('DV_MYSQL_HOST')
        DV_MYSQL_DB = getenv('DV_MYSQL_DB')
        DV_ENV = getenv('DV_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(DV_MYSQL_USER,
                                             DV_MYSQL_PWD,
                                             DV_MYSQL_HOST,
                                             DV_MYSQL_DB))
        if DV_ENV == "test":
            Base.metadata.drop_all(self.__engine)
        self.create_all()
        self._create_session()


    def _create_session(self):
        """Creates a new database session"""
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session


    def create_all(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)


    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)


    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.db_storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.db_storage.all(clas).values())
        else:
            count = len(models.db_storage.all(cls).values())

        return count
