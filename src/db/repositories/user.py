"""User repository file."""

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base, User


class UserRepo:
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        self.session = session

    async def new(
        self,
        user_id: int,
        user_name: str | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        language_code: str | None = None,
        is_premium: bool | None = False,
        user_chat: type[Base] = None,
    ) -> None:
        """Insert a new user into the database.

        :param user_id: Telegram user id
        :param user_name: Telegram username
        :param first_name: Telegram profile first name
        :param second_name: Telegram profile second name
        :param language_code: Telegram profile language code
        :param is_premium: Telegram user premium status
        :param role: User's role
        :param user_chat: Telegram chat with user.
        """
        await self.session.merge(
            User(
                user_id=user_id,
                user_name=user_name,
                first_name=first_name,
                second_name=second_name,
                language_code=language_code,
                is_premium=is_premium,
                user_chat=user_chat,
            )
        )

    async def get_by_user_id(self, user_id: int) -> User:
        """Get exactly one user by given Telegram user id."""
        return await self.session.scalar(
            select(User).where(User.user_id == user_id).limit(1)
        )

    async def update_user_name(self, user_id: int, user_name: str) -> None:
        """Update username for user by given Telegram user id."""
        await self.session.execute(
            update(User).values(user_name=user_name).where(User.user_id == user_id)
        )
