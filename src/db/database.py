""" Database class with all-in-one features """
from typing import Union

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker

from src.configuration import conf

from .repositories import ChatRepo, UserRepo


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    """
    :param url:
    :return:
    """
    return _create_async_engine(url=url, echo=conf.debug, pool_pre_ping=True)


def create_session_maker(engine: AsyncEngine = None) -> sessionmaker:
    """
    :param engine:
    :return:
    """
    return sessionmaker(
        engine or create_async_engine(conf.db.build_connection_str()),
        class_=AsyncSession,
        expire_on_commit=False,
    )


class Database:
    """
    Database class is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions
    """

    user: UserRepo
    """ User repository """
    chat: ChatRepo
    """ Chat repository """

    session: AsyncSession

    def __init__(
        self, session: AsyncSession, user: UserRepo = None, chat: ChatRepo = None
    ):
        self.session = session
        self.user = user or UserRepo(session=session)
        self.chat = chat or ChatRepo(session=session)
