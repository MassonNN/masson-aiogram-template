from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.data_structure import TransferData
from cache import Cache
from configuration import conf
from language import Translator, LocaleIdentificationMode, LocaleScheme


class TranslatorMiddleware(BaseMiddleware):
    """ This middleware throw a localized translator to handler """
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: TransferData
    ) -> Any:
        translator: Translator = data['translator']
        if conf.translate.locale_identify_mode == LocaleIdentificationMode.BY_TELEGRAM_LOCALE:
            """ Get locale from user language code """
            data['translator'] = translator(language=event.from_user.language_code)
        elif conf.translate.locale_identify_mode == LocaleIdentificationMode.BY_DATABASE:
            """ Get locale from cache """
            cache: Cache = data['cache']
            locale_key = LocaleScheme(user_id=event.from_user.id)
            # Use default locale
            locale = conf.translate.default_locale
            if await cache.exists(locale_key):
                # If any locale key were set then use it
                locale = await cache.get()
            data['translator'] = translator(language=locale)
