"""Updates for tests."""
from datetime import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Chat, Message, Update, User

TEST_USER = User(
    id=123,
    is_bot=False,
    first_name='Test',
    last_name='Bot',
    username='testbot',
    language_code='ru-RU',
    is_premium=True,
    added_to_attachment_menu=None,
    can_join_groups=None,
    can_read_all_group_messages=None,
    supports_inline_queries=None,
)

TEST_CHAT = Chat(
    id=12,
    type='private',
    title=None,
    username=TEST_USER.username,
    first_name=TEST_USER.first_name,
    last_name=TEST_USER.last_name,
    photo=None,
    bio=None,
    has_private_forwards=None,
    join_to_send_messages=None,
    join_by_request=None,
    description=None,
    invite_link=None,
    pinned_message=None,
    permissions=None,
    slow_mode_delay=None,
    message_auto_delete_time=None,
    has_protected_content=None,
    sticker_set_name=None,
    can_set_sticker_set=None,
    linked_chat_id=None,
    location=None,
)

TEST_MESSAGE = Message(message_id=123, date=datetime.now(), chat=TEST_CHAT)


def get_message(text: str, chat=TEST_CHAT, from_user=TEST_USER, **kwargs):
    """Get message update for tests."""
    return Message(
        message_id=123,
        date=datetime.now(),
        chat=chat,
        from_user=from_user,
        sender_chat=TEST_CHAT,
        text=text,
        **kwargs
    )


def get_chat(
    chat_id: int = None,
    chat_type: str = 'private',
    title: str = 'TEST_TITLE',
    username: str = TEST_CHAT.username,
    **kwargs
) -> Chat:
    """Get chat object for tests."""
    return Chat(
        id=chat_id,
        type=chat_type,
        title=title,
        username=username,
        first_name=TEST_USER.first_name,
        last_name=TEST_USER.last_name,
        **kwargs
    )


def get_callback_query(
    data: str | CallbackData, from_user=TEST_USER, message=None, **kwargs
):
    """Get callback query update for tests."""
    return CallbackQuery(
        id='test',
        from_user=from_user,
        chat_instance='test',
        message=message or TEST_MESSAGE,
        data=data,
        **kwargs
    )


def get_update(
    message: Message = None, callback_query: CallbackQuery = None, **kwargs
):
    """Get mocked update for tests."""
    return Update(
        update_id=187,
        message=message,
        callback_query=callback_query or None,
        **kwargs
    )
