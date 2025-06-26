"""This file represents a start logic."""


from aiogram import Router, types
from aiogram.filters import CommandStart

from ..utils.telegram_wrapper import telegram_wrapper

start_router = Router(name="start")


@start_router.message(CommandStart())
async def start_handler(message: types.Message):
    """Start command handler."""
    # return await message.answer('Hi, telegram!')
    # Use telegram wrapper to automatically handle exceptions like RetryAfter or ForbiddenError
    return await telegram_wrapper(message.answer, text="Hi, telegram!")
