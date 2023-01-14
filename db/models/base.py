""" Base model """
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr


@as_declarative()
class Base(object):
    """ Abstract model with declarative base functionality """
    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, auto_increment=True, primary_key=True)
