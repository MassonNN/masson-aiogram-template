from aiogram import Dispatcher

from .start import start_router


def setup_dispatcher(dp: Dispatcher):
    """ Setup dispatcher """
    dp.include_router(start_router)
