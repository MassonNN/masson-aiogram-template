""" This file represents a start logic """


from aiogram import types, Router
from aiogram.filters import CommandStart

from language.translator import LocalizedTranslator

start_router = Router(name='start')


@start_router.message(CommandStart())
async def start(message: types.Message, translator: LocalizedTranslator):
    """ Start command handler """
    return await message.answer(translator.get('welcome').format(username=message.from_user.username))
