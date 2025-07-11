import pytest

from src.core.utils import (  # путь подкорректируй под себя
    emoji_str_cancat,
    get_emoji_by_name,
)


@pytest.mark.parametrize(
    "name,expected_emoji",
    [
        ("settings", "⚙️"),
        ("search", "🔍"),
        ("overview", "🏠"),
        ("user", "👤"),
        ("info", "ℹ️"),
        ("warning", "⚠️"),
        ("check", "✅"),
        ("calendar", "📅"),
        ("email", "✉️"),
        ("phone", "📞"),
        ("lock", "🔒"),
        ("star", "⭐"),
        ("error", "❌"),
        ("fire", "🔥"),
        ("heart", "❤️"),
        ("network", "🌐"),
        ("help", "❓"),
        ("nonexistent", "❔"),  # Проверка fallback-а
        ("UNKNOWN", "❔"),  # Проверка case-insensitive
    ],
)
def test_get_emoji_by_name(name, expected_emoji):
    assert get_emoji_by_name(name) == expected_emoji


@pytest.mark.parametrize(
    "name,expected",
    [
        ("settings", "⚙️settings"),
        ("email", "✉️email"),
        ("nonexistent", "❔nonexistent"),
    ],
)
def test_emoji_str_cancat(name, expected):
    assert emoji_str_cancat(name) == expected
