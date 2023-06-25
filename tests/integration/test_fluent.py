import pytest

from language.translator import LocalizedTranslator, Translator


@pytest.fixture()
def translator():
    """
    Translator for tests
    :return:
    """
    yield Translator()


@pytest.fixture()
def localized_translator(translator: Translator):
    """Localized translator"""
    yield translator("ru")


@pytest.mark.asyncio
async def test_loc_translation(localized_translator: LocalizedTranslator):
    assert localized_translator.get("welcome", username="Тест") == "Привет, Тест!"
