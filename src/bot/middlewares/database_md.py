from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.data_structure import TransferData
from src.db.database import Database


class DatabaseMiddleware(BaseMiddleware):
    """This middleware throw a Database class to handler"""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: TransferData,
    ) -> Any:
        pool: Callable[[], AsyncSession] = data["pool"]
        session = pool()
        data["db"] = Database(session)
        try:
            return await handler(event, data)
        finally:
            await session.close()
