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
            data['translator'] = translator(language=event.from_user.language_code)
        elif conf.translate.locale_identify_mode == LocaleIdentificationMode.BY_DATABASE:
            cache: Cache = data['cache']
            data['translator'] = translator(language=await cache.get(LocaleScheme(user_id=event.from_user.id)))


