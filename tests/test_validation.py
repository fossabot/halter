from unittest.mock import MagicMock

import pytest

from src.validation import InputValidator, ValidationType


@pytest.fixture
def validator() -> InputValidator:
    page = MagicMock(spec=["open", "update"])
    return InputValidator(page)


def create_event_mock(value) -> MagicMock:
    event = MagicMock()
    event.control.value = value
    event.control.label = "Test Dropdown"
    return event


@pytest.mark.parametrize(
    "value,expected",
    [("test", True), ("", False)],
)
def test_not_empty(validator: InputValidator, value, expected: bool) -> None:
    event = create_event_mock(value)
    assert validator.validate(ValidationType.NotEmpty, event) == expected


@pytest.mark.parametrize(
    "value,expected",
    [("ValidName123", True), ("Имя", False), ("", False)],
)
def test_only_english(validator, value, expected):
    event = create_event_mock(value)
    assert validator.validate(ValidationType.OnlyEnglish, event) == expected


@pytest.mark.parametrize(
    "value,expected",
    [("value", True), (None, False)],
)
def test_dropdown_selection(validator: InputValidator, value, expected: bool) -> None:
    event: MagicMock = create_event_mock(value)
    assert validator.validate(ValidationType.NotSelected, event) == expected


@pytest.mark.parametrize(
    "value,mask,network_ip,expected",
    [
        ("192.168.1.10", 24, "192.168.1.0", True),  # обычный хост
        ("192.168.1.0", 24, "192.168.1.0", False),  # сетевой
        ("192.168.1.255", 24, "192.168.1.0", False),  # broadcast
        ("192.168.2.1", 24, "192.168.1.0", False),  # вне подсети
        ("invalid", 24, "192.168.1.0", False),  # мусор
    ],
)
def test_ipv4_host_address_full(validator: InputValidator, value, mask, network_ip, expected):
    event: MagicMock = create_event_mock(value)
    result: bool = validator.validate(
        ValidationType.IPv4HostAddress,
        event,
        parameter=mask,
        parameter2=network_ip,
    )
    assert result == expected


@pytest.mark.parametrize(
    "value,mask,expected",
    [
        ("192.168.1.0", 24, True),  # валидный адрес сети
        ("192.168.1.1", 24, False),  # не сетевой адрес
        ("invalid_ip", 24, False),  # некорректный IP
    ],
)
def test_ipv4_network_address_full(validator: InputValidator, value, mask, expected) -> None:
    event: MagicMock = create_event_mock(value)
    result = validator.validate(ValidationType.IPv4NetworkAddress, event, parameter=mask)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    [("100", True), ("0", False), ("5000", False), ("abc", False)],
)
def test_vlan_id(validator, value, expected):
    event = create_event_mock(value)
    assert validator.validate(ValidationType.VLAN, event) == expected


def test_ipv4_network_address_not_exact_network(
    validator: InputValidator,
) -> None:
    # Введённый IP не совпадает с network.network_address
    event: MagicMock = create_event_mock("192.168.1.1")
    result: bool = validator.validate(ValidationType.IPv4NetworkAddress, event, parameter="24")
    assert result is False


def test_ipv4_network_address_non_exploded_format(validator):
    # Введённый IP не в exploded формате
    event: MagicMock = create_event_mock("192.168.001.000")  # still valid IP, but != "192.168.1.0"
    result = validator.validate(ValidationType.IPv4NetworkAddress, event, parameter="24")
    assert result is False
