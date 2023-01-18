""" This file contains a translator adapter """
from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorRunner, TranslatorHub, FluentTranslator

from abstract import Adapter


LOCALES_PATH = Path(__file__).parent / 'locales'


class Translator(Adapter):
    """ This class is a translator adapter and will be used in the bot """
    translator_runner: TranslatorRunner
    translator_hub: TranslatorHub

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

    def get_text(self, key: str, language: str = 'ru'):
        """ Get text from locale with key """
        return self.translator_hub.get_translator_by_locale(locale=language).get(key)

