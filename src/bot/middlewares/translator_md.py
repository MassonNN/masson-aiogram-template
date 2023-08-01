"""Translator middleware is used for inject translator dependency in handlers."""
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.bot.structures.data_structure import TransferData
from src.cache import Cache
from src.configuration import conf
from src.language.enums import LocaleIdentificationMode
from src.language import LocaleScheme, Translator


class TranslatorMiddleware(BaseMiddleware):
    """This middleware throw a localized translator to handler."""

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        """This method is calling for every update of Message and CallbackQuery type."""
        translator: Translator = data['translator']
        if (
            conf.translate.locale_identify_mode
            == LocaleIdentificationMode.BY_TELEGRAM_LOCALE
        ):
            """Get locale from user language code"""
            data['translator'] = translator(
                language=event.from_user.language_code
            )
        elif (
            conf.translate.locale_identify_mode
            == LocaleIdentificationMode.BY_DATABASE
        ):
            """Get locale from cache"""
            cache: Cache = data['cache']
            locale_key = LocaleScheme(user_id=event.from_user.id)
            # Use default locale
            locale = conf.translate.default_locale
            if await cache.exists(locale_key):
                # If any locale key were set then use it
                locale = await cache.get(locale_key)
            data['translator'] = translator(language=locale)
