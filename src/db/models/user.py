""" User model file """
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import mapped_column

from src.bot.role import Role

from .base import Base


class User(Base):
    """
    User model
    """

    user_id = mapped_column(sa.BigInteger, unique=True, nullable=False)
    """ Telegram user id """
    user_name = mapped_column(sa.Text, unique=False, nullable=True)
    """ Telegram user name """
    first_name = mapped_column(sa.Text, unique=False, nullable=True)
    """ Telegram profile first name """
    second_name = mapped_column(sa.Text, unique=False, nullable=True)
    """ Telegram profile second name """
    language_code = mapped_column(sa.Text, unique=False, nullable=True)
    """ Telegram profile language code """
    is_premium = mapped_column(sa.Boolean, unique=False, nullable=False)
    """ Telegram user premium status """
    role = mapped_column(sa.Enum(Role), default=Role.USER)
    """ User's role """
    user_chat_fk = mapped_column(sa.ForeignKey("chat.id"), unique=False, nullable=False)
    user_chat = orm.relationship("Chat", uselist=False, lazy="joined")
    """ Telegram chat with user """
