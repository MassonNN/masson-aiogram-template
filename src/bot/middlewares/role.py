"""Role middleware used for get role of user for followed filtering."""
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from src.bot.structures.data_structure import TransferData, TransferUserData
from src.db import Database
from src.db.models import User


class RoleMiddleware(BaseMiddleware):
    """This class is used for getting user role from database."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData | TransferUserData,
    ) -> Any:
        """This method is calling for every update of Message or CallbackQuery type."""
        db: Database = data['db']
        user = await db.user.get_by_where(User.user_id == event.from_user.id)
        data['role'] = user.role
        return await handler(event, data)
