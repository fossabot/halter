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
    return emojis.get(
        name.lower(), "❔"
    )  # Возвращает ❔ если эмодзи не найден


def emoji_str_cancat(name: str) -> str:
    return get_emoji_by_name(name) + name


class Color:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"

    # Стили
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
