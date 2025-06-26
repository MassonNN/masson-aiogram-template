"""Role middleware used for get role of user for followed filtering."""
from typing import Any
from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from dishka import FromDishka
from dishka.integrations.aiogram import AiogramMiddlewareData

from src.bot.di import inject_md
from src.db import Database


class UpsertMiddleware(BaseMiddleware):
    @inject_md
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: AiogramMiddlewareData,
        db: FromDishka[Database],
    ):
        chat = event.chat
        await db.chat.new(
            chat_id=chat.id,
            chat_name=chat.username,
            chat_type=chat.type,
            title=chat.title,
        )
        await db.session.commit()
