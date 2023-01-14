""" User model file """
import sqlalchemy as sa
import sqlalchemy.orm as orm

from .base import Base
from ..role import Role


class User(Base):
    """
    User model
    """

    user_id = sa.Column(sa.BigInteger, unique=True, nullable=False)
    """ Telegram user id """
    user_name = sa.Column(sa.Text, unique=False, nullable=True)
    """ Telegram user name """
    first_name = sa.Column(sa.Text, unique=False, nullable=True)
    """ Telegram profile first name """
    second_name = sa.Column(sa.Text, unique=False, nullable=True)
    """ Telegram profile second name """
    language_code = sa.Column(sa.Text, unique=False, nullable=True)
    """ Telegram profile language code """
    is_premium = sa.Column(sa.Boolean, unique=False, nullable=False)
    """ Telegram user premium status """
    role = sa.Column(sa.Enum(Role), default=Role.USER)
    """ User's role """
    user_chat_fk = sa.Column(sa.ForeignKey('chat.id'), unique=False, nullable=False)
    user_chat = orm.relationship(
        'Chat', uselist=False, lazy='joined'
    )
    """ Telegram chat with user """
