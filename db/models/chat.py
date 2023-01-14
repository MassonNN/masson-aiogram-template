""" Chat model file """
import sqlalchemy as sa

from .base import Base


class Chat(Base):
    """
    Chat model
    """

    chat_id = sa.Column(sa.BigInteger, unique=True, nullable=False)
    """ Chat telegram id """
    chat_type = sa.Column(sa.Text, unique=False, nullable=False)
    """ Chat type can be either ‘private’, ‘group’, ‘supergroup’ or ‘channel’ """
    title = sa.Column(sa.Text, unique=False, nullable=True)
    """ Title of the chat """
    chat_name = sa.Column(sa.Text, unique=False, nullable=True)
    """ Telegram chat full name """
    chat_user = sa.Column(sa.ForeignKey('user.id'), unique=False, nullable=False)
    """ Foreign key to user (it can has effect only in private chats) """
