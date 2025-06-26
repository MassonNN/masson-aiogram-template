from aiogram.types import Chat, User


def generate_user_url_tg(user: User):
    """Genereates user url for use in html text."""
    if user.username:
        name = f"{user.full_name} (@{user.username})"
    elif len(user.full_name) >= 3:
        name = f"{user.full_name}"
    else:
        name = f"{user.id}"
    return f'<a href="tg://user?id={user.id}">{name}</a>'


def generate_chat_url_tg(chat: Chat):
    """Generates chat url for use in html text."""
    if chat.username:
        return f'<a href="https://t.me/{chat.username}/">{chat.title}</a>'
    return f"{chat.title}"


def message_link(chat_id: int, text: str, message_id: int):
    """Generates link to a message, transforming telegram chat id to client peer id."""
    return (
        f'<a href="https://t.me/c/{-(chat_id + 1000000000000)}/{message_id}">{text}</a>'
    )


def message_link_by_name(chat_name: str, text: str, message_id: int):
    """Generates link to a message with chat username
    :param chat_name: Telegram chat username (@username)
    :param text: Link placeholder text
    :param message_id: Message id.
    """
    return f'<a href="https://t.me/{chat_name}/{message_id}">{text}</a>'
