"""Tests for LocaleScheme."""
from src.language.enums import Locales
from src.language.translator import LocaleScheme


def test_generate_scheme():
    """Check if LocaleScheme generates correctly."""
    str_value = Locales.RU.value
    lc = LocaleScheme(user_id=1, locale=Locales.RU)
    assert str(lc) == str_value

    new_lc = LocaleScheme.from_value(key='locale:1', value=str_value)
    assert new_lc == lc
