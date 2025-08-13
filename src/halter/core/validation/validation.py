# core/validation/validation.py

import re

from halter.core.constants import DEVICE_ROLES


def validate_netbios_name(name: str) -> None:
    """
    Проверяет, что имя соответствует требованиям NetBIOS:
    - длина от 1 до 15 символов
    - только латинские буквы, цифры и дефис
    """
    pattern = r"^[A-Za-z0-9-]{1,15}$"
    if not re.fullmatch(pattern, name):
        raise ValueError(f"Invalid NetBIOS name: {name}")


def validate_role(role: str) -> None:
    """
    Валидирует роль среди предопределенных ролей
    """
    if role not in DEVICE_ROLES:
        raise ValueError(f"Invalid device role: {role}")
