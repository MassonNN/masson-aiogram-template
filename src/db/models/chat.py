"""Chat model file."""
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Chat(Base):
    """Chat model."""

    chat_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False
    )
    """ Chat telegram id """
    chat_type: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=False
    )
    """ Chat type can be either ‘private’, ‘group’, ‘supergroup’ or ‘channel’ """
    title: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)
    """ Title of the chat """
    chat_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    """ Telegram chat full name """
    chat_user: Mapped[int] = mapped_column(
        sa.ForeignKey('user.id', ondelete='CASCADE'),
        unique=False,
        nullable=True,
    )
    """ Foreign key to user (it can has effect only in private chats) """
