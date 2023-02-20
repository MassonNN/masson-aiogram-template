"""
This file contains TypedDict structure to store data which will
transfer throw Dispatcher->Middlewares->Handlers
"""

from typing import TypedDict, Callable

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.role import Role
from cache import Cache
from db.database import Database
from language import Translator
from language.translator import LocalizedTranslator


class TransferData(TypedDict):
    translator: Translator | LocalizedTranslator
    pool: Callable[[], AsyncSession]
    db: Database
    bot: Bot
    cache: Cache


class TransferUserData(TypedDict):
    role: Role

