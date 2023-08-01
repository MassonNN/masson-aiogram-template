"""Role middleware used for get role of user for followed filtering."""
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from src.bot.structures.data_structure import TransferData
from src.db import Database


class RoleMiddleware(BaseMiddleware):
    """This class is used for getting user role from database."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        """This method calls each update of Message or CallbackQuery type."""
        db: Database = data['db']
        data['role'] = await db.user.get_role()
        return await handler(event, data)
