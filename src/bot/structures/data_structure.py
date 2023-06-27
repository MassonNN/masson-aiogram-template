"""Data Structures.

This file contains TypedDict structure to store data which will
transfer throw Dispatcher->Middlewares->Handlers.
"""

from collections.abc import Callable
from typing import TypedDict

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role
from src.cache import Cache
from src.db.database import Database
from src.language.enums import Locales
from src.language.translator import LocalizedTranslator, Translator


class TransferData(TypedDict):
    """Common transfer data."""

    translator: Translator | LocalizedTranslator
    pool: Callable[[], AsyncSession]
    db: Database
    bot: Bot
    cache: Cache


class TransferUserData(TypedDict):
    """Transfer data associated with user."""

    role: Role
    locale: Locales
