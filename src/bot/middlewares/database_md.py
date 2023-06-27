"""Database middleware is a common way to inject database dependency
in handlers."""
from typing import Any
from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.bot.structures.data_structure import TransferData
from src.db.database import Database


class DatabaseMiddleware(BaseMiddleware):
    """This middleware throw a Database class to handler."""

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        """This method is calling for every update"""
        async with data["pool"] as session:  # type: AsyncSession
            data["db"] = Database(session)
            return await handler(event, data)
