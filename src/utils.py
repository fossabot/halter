def get_emoji_by_name(name: str) -> str:
    emojis: dict[str, str] = {
        "settings": "⚙️",
        "search": "🔍",
        "overview": "🏠",
        "user": "👤",
        "info": "ℹ️",
        "warning": "⚠️",
        "check": "✅",
        "calendar": "📅",
        "email": "✉️",
        "phone": "📞",
        "lock": "🔒",
        "star": "⭐",
        "error": "❌",
        "fire": "🔥",
        "heart": "❤️",
        "network": "🌐",
        "help": "❓",
    }
    return emojis.get(name.lower(), "❔")  # Возвращает ❔ если эмодзи не найден


def emoji_str_cancat(name: str) -> str:
    return get_emoji_by_name(name) + name
