import enum


class LocaleIdentificationMode(enum.Enum):
    """Locale indetification modes"""

    BY_TELEGRAM_LOCALE = enum.auto()
    """ With this mode translator will use Message.from_user.language_code to identify language 
        Warning! Do not use this mode if you doesn't confident in it     
    """
    BY_DATABASE = enum.auto()
    """ With this mode translator will use database (redis) to get locale. 
    You have to set locales as soon as possible """


class Locales(str, enum.Enum):
    """Locales supported by app"""

    EN = "en"
    RU = "ru"
    UK = "uk"
