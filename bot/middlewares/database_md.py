from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.data_structure import TransferData
from db.database import Database


class DatabaseMiddleware(BaseMiddleware):
    """ This middleware throw a Database class to handler """
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: TransferData
    ) -> Any:
        pool: Callable[[], AsyncSession] = data['pool']
        session = pool()
        data['db'] = Database(session)
        try:
            return await handler(event, data)
        finally:
            await session.close()