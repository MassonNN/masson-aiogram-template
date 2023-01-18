"""
This file contains TypedDict structure to store data which will
transfer throw Dispatcher->Middlewares->Handlers
"""

from typing import TypedDict

from aiogram import Bot

from cache import Cache
from db.database import Database
from language import Translator
from language.translator import LocalizedTranslator


class TransferData(TypedDict):
    translator: Translator | LocalizedTranslator
    db: Database
    bot: Bot
    cache: Cache
