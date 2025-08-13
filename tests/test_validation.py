# tests/test_netbios_validator.py

import pytest

from halter.core.validation.validation import validate_netbios_name


@pytest.mark.parametrize(
    "valid_name",
    [
        "SERVER01",
        "My-Host",
        "A",  # минимальная длина
        "123456789012345",  # длина 15
    ],
)
def test_validate_netbios_name_valid(valid_name: str) -> None:
    # не должно бросать ошибок
    validate_netbios_name(valid_name)


@pytest.mark.parametrize(
    "invalid_name",
    [
        "",  # пустая строка
        "TOO_LONG_NAME_123",  # длина > 15
        "Invalid_Name!",  # недопустимый символ '!'
        "with space",  # пробелы не разрешены
        "_underscore",  # первый символ '_' не входит в [A-Za-z0-9-]
    ],
)
def test_validate_netbios_name_invalid(invalid_name: str) -> None:
    with pytest.raises(ValueError) as exc:
        validate_netbios_name(invalid_name)
    assert "Invalid NetBIOS name" in str(exc.value)
