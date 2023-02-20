from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class RoleMiddleware(BaseMiddleware):
    """
    This class is used for getting user role from database
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: TransferUserData
    ) -> Any:
        ...