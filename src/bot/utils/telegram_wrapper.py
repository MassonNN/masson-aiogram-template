import asyncio
import logging
from collections.abc import Awaitable, Callable

from aiogram.exceptions import (TelegramBadRequest, TelegramForbiddenError,
                                TelegramMigrateToChat, TelegramNetworkError,
                                TelegramRetryAfter)


async def telegram_wrapper(
    func: Callable | Awaitable, handle: bool = False, *args, **kwargs
):
    """This function wraps telegram method to provide regular exceptions handling
    :param func: Telegram method
    :param handle: If true returns exception object for handling in business logic.
    """
    try:
        return await func(*args, **kwargs)
    except TelegramBadRequest as tbr:
        if handle:
            return tbr
        logging.error(tbr.message + " on method " + str(func))
        return None
    except TelegramNetworkError as tne:
        if handle:
            return tne
        logging.error(tne.message + " on method " + str(func))
        return None
    except TelegramMigrateToChat as tmt:
        kwargs["chat_id"] = tmt.migrate_to_chat_id
        logging.warning(tmt.message)
        return await telegram_wrapper(func, *args, **kwargs)
    except TelegramRetryAfter as tra:
        logging.warning(f"TelegramRetryAfter: {tra.retry_after}")
        await asyncio.sleep(tra.retry_after)
        return await telegram_wrapper(func, *args, **kwargs)
    except TelegramForbiddenError as tbe:
        if handle:
            return tbe
        logging.error(tbe.message + " on method " + str(func))
        return None
