""" This file contains build dispatcher logic """
from aiogram import Dispatcher

from bot.middlewares.translator_md import TranslatorMiddleware
from logic import routers


def setup_dispatcher(dp: Dispatcher):
    """ This function set up dispatcher with routers, filters and middlewares """
    for router in routers:
        dp.include_router(router)
    dp.message.middleware(TranslatorMiddleware())
    dp.callback_query.middleware(TranslatorMiddleware())
    return dp
