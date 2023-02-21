""" This file represents a start logic """


from aiogram import Router, types
from aiogram.filters import Command

from src.language.translator import LocalizedTranslator

help_router = Router(name="help")


@help_router.message(Command(commands="help"))
async def help(message: types.Message, translator: LocalizedTranslator):
    """Help command handler"""
    return await message.answer(translator.get("start"))
