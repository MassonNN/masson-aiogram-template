""" This file represents a start logic """


from aiogram import types, Router
from aiogram.filters import CommandStart

start_router = Router(name='start')
start_router.message.filter()


@start_router.message(CommandStart())
async def start(message: types.Message):
    """ Start command handler """
    return await message.answer()
