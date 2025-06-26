"""Chat repository file."""

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Chat


class ChatRepo:
    """Chat repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize chat repository as for all chats or only for one chat."""
        self.session = session

    async def new(
        self,
        chat_id: int,
        chat_type: str,
        title: str,
        chat_name: str,
    ) -> Chat:
        """Insert a new chat into the database."""
        new_chat = await self.session.merge(
            Chat(
                chat_id=chat_id,
                chat_type=chat_type,
                title=title,
                chat_name=chat_name,
            )
        )
        return new_chat

    async def get_by_chat_id(self, chat_id: int) -> Chat:
        """Get exactly one chat by given Telegram chat id."""
        return await self.session.scalar(
            select(Chat).where(Chat.chat_id == chat_id).limit(1)
        )

    async def update_chat_title(self, chat_id: int, new_title: str) -> None:
        await self.session.execute(
            update(Chat).values(title=new_title).where(Chat.chat_id == chat_id)
        )
