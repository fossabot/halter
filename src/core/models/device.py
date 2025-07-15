from dataclasses import dataclass, field

from core.constants import DEVICE_ROLES

from .interface import NetworkInterface


@dataclass(slots=True, kw_only=True)
class Device:
    name: str  # NetBIOS
    description: str
    role: DEVICE_ROLES
    interfaces: list[NetworkInterface] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.name) > 15:
            raise ValueError("NetBIOS name must be 15 characters or fewer.")
