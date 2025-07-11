APP_NAME: str = "Halter"
DEFAULT_PATH = "project.yaml"

PROJECT_CUSTOMER: list[str] = ["Transneft", "Other"]
PROJECT_TYPES: list[str] = ["MNS", "SAR", "PT", "ASME", "PNS", "RP"]
PROJECT_STAGES: list[str] = [
    "Tender",  # Тендер
    "Planning",  # Подбор спецификации
    "Design",  # Разработка проекта
    "Implementation",  # Альфа-тестирование
    "Internal Testing",  # Заводские испытания с заказчиком
    "External Testing",  # Испытания ЦПА
    "Commissioning works",  # ПНР
    "Completed",  # Завершение проекта
]

DEVICE_ROLES: list[str] = [
    "Router",  # Маршрутизатор
    "Switch",  # Коммутатор
    "Panel",  # Панель сигнализации
    "Timeserver",  # Сервер точного времени
    "Workstation",  # АРМ
    "DMZ",  # Сервер демилитаризованной зоны
]

DEVICE_BRANDS: list[str] = ["Moxa", "Zelax", "HP", "iROBO"]

NETWORK_ADDRESS_CLASS: list[str] = ["A", "B", "C"]

COLORS: list[dict[str, str]] = [
    {"bg": "#4CAF50", "text": "white"},  # Green
    {"bg": "#2196F3", "text": "white"},  # Blue
    {"bg": "#FF9800", "text": "black"},  # Orange
    {"bg": "#9C27B0", "text": "white"},  # Purple
    {"bg": "#03A9F4", "text": "black"},  # Light Blue
    {"bg": "#E91E63", "text": "white"},  # Pink
    {"bg": "#607D8B", "text": "white"},  # Blue Grey
    {"bg": "#FFC107", "text": "black"},  # Amber
]
