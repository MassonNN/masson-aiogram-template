"""
This file contains TypedDict structure to store data which will
transfer throw Dispatcher->Middlewares->Handlers
"""

from typing import TypedDict

from aiogram import Bot

from cache import Cache
from db.database import Database
from language import Translator


class TransferData(TypedDict):
    translator: Translator
    db: Database
    bot: Bot
    cache: Cache
