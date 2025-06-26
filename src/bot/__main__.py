"""This file represent startup bot logic."""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from .di import InfrastructureProvider, FSMStorageProvider, ConfigurationProvider
from ..bot.dispatcher import setup_dispatcher
from ..configuration import Configuration
from ..db.di import DatabaseProvider


async def start_bot():
    """This function will start bot with polling mode."""
    container = make_async_container(
        DatabaseProvider(),
        InfrastructureProvider(),
        FSMStorageProvider(),
        ConfigurationProvider()
    )
    conf = await container.get(Configuration)
    storage = await container.get(BaseStorage)
    dp = Dispatcher(storage=storage)
    setup_dishka(container=container, router=dp)
    setup_dispatcher(dp)

    bot = Bot(token=conf.bot.token)
    logging.basicConfig(level=conf.logging_level)

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


if __name__ == '__main__':
    asyncio.run(start_bot())
