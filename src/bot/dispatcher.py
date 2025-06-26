"""This file contains build dispatcher logic."""
from aiogram import Dispatcher

from .logic import routers


def setup_dispatcher(dp: Dispatcher):
    """This function set up dispatcher with routers, filters and middlewares."""
    for router in routers:
        dp.include_router(router)

    # Register middlewares

    return dp
