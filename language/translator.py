""" This file contains a translator adapter """
from copy import copy
from pathlib import Path
from typing import NamedTuple

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorRunner, TranslatorHub, FluentTranslator

from abstract import Adapter


LOCALES_PATH = Path(__file__).parent / 'locales'


class Translator(Adapter):
    """ This class is a translator adapter and will be used in the bot """
    translator_runner: TranslatorRunner
    translator_hub: TranslatorHub

    language: str

    def __init__(self):
        self.translator_hub = TranslatorHub(
            locales_map={
                "ru": ("ru", ),
            },
            translators=[
                FluentTranslator(
                    locale='ru',
                    translator=FluentBundle.from_files(
                        locale='ru-RU',
                        filenames=[LOCALES_PATH / 'ru.ftl', ]
                    )
                )
            ]
        )

    def get_text(self, key: str, language: str = None):
        """ Get text from locale with key """
        return self.translator_hub.get_translator_by_locale(
            locale=language or self.language
        ).get(key)

    def __call__(self, language: str, *args, **kwargs):
        _to_ret = copy(self)
        _to_ret.language = language
        return _to_ret


class LocaleScheme(NamedTuple):
    """ Locale scheme for presentate a cache locale key """
    user_id: int
    locale: str

    def __str__(self):
        return f"{self.user_id}:{self.locale}"
