from dataclasses import dataclass, field

from core.constants import DEVICE_ROLES
from core.validation.validation import validate_netbios_name

from .interface import NetworkInterface


@dataclass(slots=True, kw_only=True)
class Device:
    name: str  # NetBIOS
    description: str
    model: str
    role: DEVICE_ROLES
    interfaces: list[NetworkInterface] = field(default_factory=list)

    def __post_init__(self) -> None:
        validate_netbios_name(self.name)
