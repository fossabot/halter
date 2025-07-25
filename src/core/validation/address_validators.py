# address_validation.py
"""Унифицированная валидация через регулярные шаблоны"""

import ipaddress
import re

from core.models.address import AddressingType

_validation_patterns: dict[AddressingType, tuple[str, str]] = {
    AddressingType.OPC_UA_ADDRESS: (
        r"^opc\.tcp://[\w.-]+(:\d+)?(/.*)?$",
        "OPC UA address",
    ),
    AddressingType.DNS_NAME: (
        r"^[\w]([\w\-]{0,61}[\w])?(\.[\w]([\w\-]{0,61}[\w])?)*$",
        "DNS name",
    ),
    AddressingType.HTTP_URL: (r"^https?://[\w.-]+(:\d+)?(/.*)?$", "HTTP URL"),
    AddressingType.EMAIL_ADDRESS: (
        r"^[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,}$",
        "email",
    ),
}


def _validate_with_pattern(addr: str, pattern: str, desc: str) -> None:
    if not re.match(pattern, addr):
        raise ValueError(f"Invalid {desc}: {addr}")


# Простые валидаторы


def _validate_ipv4_network(addr: str) -> None:
    try:
        ipaddress.ip_network(addr, strict=False)
    except ValueError as e:
        raise ValueError(f"Invalid IPv4 network: {addr}") from e


def _validate_ipv4_address(addr: str) -> None:
    try:
        ipaddress.ip_address(addr)
    except ValueError as e:
        raise ValueError(f"Invalid IPv4 address: {addr}") from e


def _validate_slaveid(addr: str) -> None:
    if not (addr.isdigit() and 0 <= int(addr) <= 247):
        raise ValueError(f"Slave ID must be integer 0-247: {addr}")


def _validate_analog_signal(addr: str) -> None:
    if not re.match(r"^(?:\d+-\d+(?:mA|V)|\d+%)$", addr):
        raise ValueError(f"Invalid analog signal: {addr}")


# Словарь валидаторов
VALIDATION_FUNCTIONS: dict[AddressingType, callable] = {
    AddressingType.ANALOG_SIGNAL: _validate_analog_signal,
    AddressingType.MODBUS_RTU_ADDRESS: _validate_slaveid,
    AddressingType.IP_NETWORK: _validate_ipv4_network,
    AddressingType.IP_ADDRESS: _validate_ipv4_address,
    AddressingType.OPC_UA_ADDRESS: lambda a: _validate_with_pattern(
        a, *_validation_patterns[AddressingType.OPC_UA_ADDRESS]
    ),
    AddressingType.MES_TAG_ADDRESS: lambda a: _validate_with_pattern(
        a, r"^[A-Za-z][\w_]*(?:\.[A-Za-z][\w_]*){1,3}$", "MES tag"
    ),
    AddressingType.DNS_NAME: lambda a: _validate_with_pattern(
        a, *_validation_patterns[AddressingType.DNS_NAME]
    ),
    AddressingType.SCADA_TAG_ADDRESS: lambda a: _validate_with_pattern(
        a, r"^[A-Za-z][\w_]*(?:\.[A-Za-z][\w_]*)*$", "SCADA tag"
    ),
    AddressingType.HTTP_URL: lambda a: _validate_with_pattern(
        a, *_validation_patterns[AddressingType.HTTP_URL]
    ),
    AddressingType.EMAIL_ADDRESS: lambda a: _validate_with_pattern(
        a, *_validation_patterns[AddressingType.EMAIL_ADDRESS]
    ),
    AddressingType.DATABASE_CONNECTION: lambda a: True
    if any(
        p in a.lower()
        for p in ("server=", "host=", "data source=", "database=")
    )
    else (_ for _ in ()).throw(ValueError(f"Invalid DB connection: {a}")),
}
