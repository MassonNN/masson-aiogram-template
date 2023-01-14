""" Chat repository file """

from sqlalchemy.orm import sessionmaker

from .repository import Repository
from ..models import Chat as _Chat, User as _User


class Chat(Repository):
    """
    Chat repository for CRUD and other SQL queries
    """

    def __init__(self, pool: sessionmaker, chat: _Chat = None):
        """
        Initialize chat repository as for all chats or only for one chat

        :param chat: (Optional) Specify which chat model will be manipulated
        """
        super().__init__(type_model=_Chat, pool=pool)
        self.model = chat

    def __call__(self, *args, **kwargs):
        chat = kwargs.get('chat')
        pool = kwargs.get('pool')
        return self.__class__(pool, chat)

    async def new(
            self,
            chat_id: int,
            chat_type: str,
            title: str,
            chat_name: str,
            chat_user: _User,
    ) -> None:
        """
        Insert a new user into the database
        """
        async with self.pool() as session:
            session.add(_Chat(
                chat_id=chat_id,
                chat_type=chat_type,
                title=title,
                chat_name=chat_name,
                chat_user=chat_user
            ))
            await session.commit()
