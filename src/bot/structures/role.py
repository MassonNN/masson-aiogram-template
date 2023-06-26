"""Roles."""

import enum


class Role(enum.IntEnum):
    """You can change these roles as you want."""

    USER = 0
    MODERATOR = 1
    ADMINISTRATOR = 2
