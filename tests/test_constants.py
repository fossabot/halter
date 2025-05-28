from src.constants import (
    APP_NAME,
    COLORS,
    DEVICE_BRANDS,
    DEVICE_ROLES,
    PROJECT_CUSTOMER,
    PROJECT_STAGES,
    PROJECT_TYPES,
)


def test_app_name() -> None:
    assert isinstance(APP_NAME, str)
    assert APP_NAME == "Halter"


def test_project_customer() -> None:
    assert PROJECT_CUSTOMER == ["Transneft", "Other"]


def test_project_types() -> None:
    assert "MNS" in PROJECT_TYPES
    assert "Other" in PROJECT_TYPES
    assert len(PROJECT_TYPES) >= 5


def test_project_stages() -> None:
    expected: list[str] = [
        "Tender",
        "Planning",
        "Design",
        "Implementation",
        "Internal Testing",
        "External Testing",
        "Commissioning works",
        "Completed",
    ]
    assert PROJECT_STAGES == expected


def test_device_roles() -> None:
    expected_roles: set[str] = {
        "Router",
        "Switch",
        "Panel",
        "Timeserver",
        "Workstation",
        "DMZ",
    }
    assert set(DEVICE_ROLES) == expected_roles


def test_device_brands() -> None:
    assert DEVICE_BRANDS == ["Moxa", "Zelax", "HP", "iROBO"]


def test_colors_format_and_count() -> None:
    assert len(COLORS) == 8
    for color in COLORS:
        assert isinstance(color, dict)
        assert "bg" in color and "text" in color
        assert isinstance(color["bg"], str)
        assert isinstance(color["text"], str)
