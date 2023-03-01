from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.bot.structures.data_structure import TransferData
from src.cache import Cache
from src.configuration import conf
from src.language.translator import LocaleScheme, Translator
from src.language.enums import LocaleIdentificationMode


class TranslatorMiddleware(BaseMiddleware):
    """This middleware throw a localized translator to handler"""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: TransferData,
    ) -> Any:
        translator: Translator = data["translator"]
        if (
            conf.translate.locale_identify_mode
            == LocaleIdentificationMode.BY_TELEGRAM_LOCALE
        ):
            """Get locale from user language code"""
            data["translator"] = translator(language=event.from_user.language_code)
        elif (
            conf.translate.locale_identify_mode == LocaleIdentificationMode.BY_DATABASE
        ):
            """Get locale from cache"""
            cache: Cache = data["cache"]
            locale_key = LocaleScheme(user_id=event.from_user.id)
            # Use default locale
            locale = conf.translate.default_locale
            if await cache.exists(locale_key):
                # If any locale key were set then use it
                locale = await cache.get(locale_key)
            data["translator"] = translator(language=locale)
