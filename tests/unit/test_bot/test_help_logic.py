import pytest

from unittest.mock import AsyncMock
from aiogram.types import Message

from bot.logic.help import help as _help
from language.translator import LocalizedTranslator
from tests.utils.updates import TEST_USER

TEST_TEXT = 'test_text'


@pytest.mark.asyncio
async def test_help_response():
    mocked_translator = AsyncMock(LocalizedTranslator)
    mocked_message = AsyncMock(Message)
    mocked_message.from_user = TEST_USER
    mocked_message.answer = AsyncMock()
    mocked_translator.configure_mock(**{
        'get.return_value': TEST_TEXT,
    })

    await _help(mocked_message, mocked_translator)

    mocked_message.answer.assert_awaited_once_with(TEST_TEXT)
    mocked_translator.get.assert_called_once_with('help')

