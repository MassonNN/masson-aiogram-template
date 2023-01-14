""" This file represent startup bot logic"""
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from language.translator import Translator
from .logic import setup_dispatcher
from configuration import conf


async def start_bot():
    """ This function will start bot with polling mode """
    bot = Bot(token=conf.bot.token)
    dp = Dispatcher(
        storage=RedisStorage(
            redis=Redis(
                host=conf.redis.host,
                password=conf.redis.passwd,
                username=conf.redis.username,
                db=conf.redis.db
            ), state_ttl=conf.redis.state_ttl, data_ttl=conf.redis.data_ttl
        )
    )
    setup_dispatcher(dp)

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        translator=Translator()
    )


if __name__ == '__main__':
    pass
