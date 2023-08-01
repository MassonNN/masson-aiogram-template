"""User model file."""
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from src.bot.structures.role import Role

from .base import Base
from .chat import Chat


class User(Base):
    """User model."""

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False
    )
    """ Telegram user id """
    user_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    """ Telegram user name """
    first_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    """ Telegram profile first name """
    second_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    """ Telegram profile second name """
    is_premium: Mapped[bool] = mapped_column(
        sa.Boolean, unique=False, nullable=False
    )
    """ Telegram user premium status """
    role: Mapped[Role] = mapped_column(sa.Enum(Role), default=Role.USER)
    """ User's role """
    user_chat_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('chat.id'), unique=False, nullable=False
    )
    user_chat: Mapped[Chat] = orm.relationship(
        'Chat', uselist=False, lazy='joined'
    )
    """ Telegram chat with user """
