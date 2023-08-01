"""Tests for translator service."""
import pytest

from language.translator import LocalizedTranslator, Translator


@pytest.fixture()
def translator():
    """Translator for tests."""
    yield Translator()


@pytest.fixture()
def localized_translator(translator: Translator):
    """Localized translator."""
    yield translator('ru')


@pytest.mark.asyncio
async def test_loc_translation(localized_translator: LocalizedTranslator):
    """Check if translator gets correct translation."""
    assert localized_translator.get(key='welcome') == 'Привет!'
