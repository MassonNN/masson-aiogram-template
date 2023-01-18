""" Database class with all-in-one features """
from typing import Union

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine as _create_async_engine, AsyncSession

from abstract.facade import Facade
from configuration import conf
from .repositories import Chat, User, Repository


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    """
    :param url:
    :return:
    """
    return _create_async_engine(url=url, echo=conf.debug, encoding='utf-8', pool_pre_ping=True)


def create_session_maker(engine: AsyncEngine = None) -> sessionmaker:
    """
    :param engine:
    :return:
    """
    return sessionmaker(
        engine or create_async_engine(
            conf.db.build_connection_str()
        ),
        class_=AsyncSession, expire_on_commit=False
    )


class Database(Facade):
    """
    Database class is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions
    """

    user: User
    """ User repository """
    chat: Chat
    """ Chat repository """

    def __init__(self, pool: sessionmaker = None, user: Repository = None, chat: Repository = None):
        self.pool = pool or create_session_maker()
        self.user = user or User(pool)
        self.chat = chat or Chat(pool)
