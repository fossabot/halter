# test/test_constants.py

import pytest

from src.core.constants import (
    COLORS,
    DEVICE_BRANDS,
    NETWORK_ADDRESS_CLASS,
    NETWORK_DIRECTION,
    NETWORK_PROTOCOLS,
    NETWORK_TIER,
    NETWORK_ZONE,
    PROJECT_CUSTOMER,
    PROJECT_STAGES,
    PROJECT_TYPES,
)

ALL_CONSTANT_LISTS = [
    PROJECT_CUSTOMER,
    PROJECT_TYPES,
    PROJECT_STAGES,
    DEVICE_BRANDS,
    NETWORK_ADDRESS_CLASS,
    NETWORK_PROTOCOLS,
    NETWORK_DIRECTION,
    NETWORK_TIER,
    NETWORK_ZONE,
]


@pytest.mark.parametrize("const_list", ALL_CONSTANT_LISTS)
def test_no_duplicates_and_no_empty(const_list):
    assert len(const_list) == len(set(const_list)), (
        f"Duplicates in {const_list}"
    )
    assert all(const_list), f"Empty string in {const_list}"


def test_colors_format_and_values() -> None:
    for color in COLORS:
        assert isinstance(color, dict)
        assert "bg" in color and "text" in color
        assert isinstance(color["bg"], str)
        assert isinstance(color["text"], str)
