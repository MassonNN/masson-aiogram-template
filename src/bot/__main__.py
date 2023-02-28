""" This file represent startup bot logic"""
import asyncio
import logging

from aiogram import Bot

from src.bot.structures.data_structure import TransferData
from src.bot.dispatcher import get_dispatcher, get_redis_storage
from src.cache import Cache
from src.configuration import conf
from src.db.database import Database
from src.language.translator import Translator


async def start_bot():
    """This function will start bot with polling mode"""
    bot = Bot(token=conf.bot.token)
    cache = Cache()
    storage = get_redis_storage(redis=cache)
    dp = get_dispatcher(storage=storage)

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(db=Database(), translator=Translator(), cache=cache)
    )


if __name__ == "__main__":
    logging.basicConfig(level=conf.logging_level)
    asyncio.run(start_bot())
