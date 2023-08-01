"""This file represents a start logic."""


from aiogram import Router, types
from aiogram.filters import CommandStart

start_router = Router(name='start')


@start_router.message(CommandStart())
async def start_handler(message: types.Message):
    """Start command handler."""
    return await message.answer('Hi, telegram!')
