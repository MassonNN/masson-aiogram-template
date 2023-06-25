""" This file contains a translator adapter """
import typing
from pathlib import Path
from typing import NamedTuple

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub, TranslatorRunner

from src.configuration import conf
from src.language.enums import Locales

LOCALES_PATH = Path(__file__).parent / "locales"


class Translator:
    """This class is a translator adapter and will be used in the bot"""

    translator_runner: TranslatorRunner
    translator_hub: TranslatorHub

    language: str

    def __init__(self):
        self.translator_hub = TranslatorHub(
            root_locale="ru",
            locales_map={
                "ru": ("ru",),
            },
            translators=[
                FluentTranslator(
                    locale="ru",
                    translator=FluentBundle.from_files(
                        locale="ru-RU",
                        filenames=[
                            LOCALES_PATH / "ru.ftl",
                        ],
                    ),
                )
            ],
        )

    def get_text(self, key: str, language: Locales = conf.default_locale):
        """Get text from locale with key"""
        return self.translator_hub.get_translator_by_locale(
            locale=language or self.language
        ).get(key)

    def __call__(self, language: str, *args, **kwargs):
        """When instance calles it's produces LocalizedTranslator"""
        return LocalizedTranslator(
            translator=self.translator_hub.get_translator_by_locale(
                locale=language or self.language
            )
        )


class LocalizedTranslator:
    """This class produced by Translator"""

    translator: TranslatorRunner

    def __init__(self, translator: TranslatorRunner):
        self.translator = translator

    def get(self, key: str, *args, **kwargs) -> str:
        """
        Get translated text with key
        :param key:
        :return:
        """
        return self.translator.get(key, *args, **kwargs)


class LocaleScheme(NamedTuple):
    """Locale scheme for presentate a cache locale key"""

    user_id: int
    locale: Locales = conf.default_locale

    def as_value(self):
        """Method to give value for store"""
        return self.locale.value

    def as_key(self):
        """Method to give key for store"""
        return f"locale:{self.user_id}"

    def __eq__(self, other):
        return (self.user_id == other.user_id) and (self.locale == other.locale)

    def __str__(self):
        return self.as_value()

    @classmethod
    def from_value(cls, key: str, value: str):
        """Method that generating LocaleScheme from value and key"""
        return cls(user_id=int(key.split(":")[1]), locale=Locales(value))

    @classmethod
    def is_locale_scheme(cls, key: str):
        return len(split := key.split(":")) == 2 and split[0] == "locale"
