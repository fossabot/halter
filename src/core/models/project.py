from dataclasses import dataclass, field

from core.constants import PROJECT_TYPES

from .device import Device
from .network import Network
from .software import Software


@dataclass(slots=True, kw_only=True)
class Project:
    name: str
    description: str
    area_type: list[str]
    networks: list[Network] = field(default_factory=list)
    devices: list[Device] = field(default_factory=list)
    software: list[Software] = field(default_factory=list)

    def __post_init__(self) -> None:
        if set(self.area_type).issubset(set(PROJECT_TYPES)):
            raise ValueError("Area type must be of from predefined values.")
