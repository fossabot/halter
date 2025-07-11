from dataclasses import dataclass, field
from typing import Literal

from .interface import NetworkInterface


@dataclass(slots=True, kw_only=True)
class Device:
    name: str  # NetBIOS
    description: str
    role: Literal["router", "switch", "ntp server", "workstation", "panel"]
    interfaces: list[NetworkInterface] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.name) > 15:
            raise ValueError("NetBIOS name must be 15 characters or fewer.")
