""" This file represent startup bot logic"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from src.bot.data_structure import TransferData
from src.bot.dispatcher import setup_dispatcher
from src.cache import Cache
from configuration import conf
from src.db.database import Database
from src.language.translator import Translator


async def start_bot():
    """ This function will start bot with polling mode """
    cache = Cache()

    bot = Bot(token=conf.bot.token)
    dp = Dispatcher(
        storage=RedisStorage(
            redis=cache.client, state_ttl=conf.redis.state_ttl, data_ttl=conf.redis.data_ttl
        )
    )
    setup_dispatcher(dp)

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(
            db=Database(),
            translator=Translator(),
            cache=cache
        )
    )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if conf.debug else logging.INFO
    )
    asyncio.run(start_bot())
