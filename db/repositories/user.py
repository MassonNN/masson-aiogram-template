""" User repository file """
from typing import Type, Optional

from sqlalchemy.orm import sessionmaker

from .repository import Repository
from ..models import User as _User, Base
from ..role import Role


class User(Repository[_User]):
    """
    User repository for CRUD and other SQL queries
    """

    def __init__(self, pool: sessionmaker, user: _User = None):
        """
        Initialize user repository as for all users or only for one user

        :param user: (Optional) Specify which user model will be manipulated
        """
        super().__init__(type_model=_User, pool=pool)
        self.model = user

    def __call__(self, *args, **kwargs):
        user = kwargs.get('user')
        pool = kwargs.get('pool')
        return self.__class__(pool, user)

    async def new(
            self,
            user_id: int,
            user_name: Optional[str] = None,
            first_name: Optional[str] = None,
            second_name: Optional[str] = None,
            language_code: Optional[str] = None,
            is_premium: Optional[bool] = False,
            role: Optional[Role] = Role.USER,
            user_chat: Type[Base] = None
    ) -> None:
        """
        Insert a new user into the database
        :param user_id: Telegram user id
        :param user_name: Telegram username
        :param first_name: Telegram profile first name
        :param second_name: Telegram profile second name
        :param language_code: Telegram profile language code
        :param is_premium: Telegram user premium status
        :param role: User's role
        :param user_chat: Telegram chat with user
        """
        async with self.pool() as session:
            session.add(_User(
                user_id=user_id,
                user_name=user_name,
                first_name=first_name,
                second_name=second_name,
                language_code=language_code,
                is_premium=is_premium,
                role=role,
                user_chat=user_chat
            ))
            await session.commit()
