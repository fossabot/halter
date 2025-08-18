from dataclasses import dataclass, field

from halter.core.constants import PROJECT_TYPES
from halter.core.models.area import Area
from halter.core.models.device import Device
from halter.core.models.network import Network
from halter.core.models.software import Software


@dataclass(slots=True, kw_only=True)
class Project:
    name: str
    description: str
    area_type: list[str] = field(default_factory=list)
    networks: list[Network] = field(default_factory=list)
    devices: list[Device] = field(default_factory=list)
    software: list[Software] = field(default_factory=list)
    areas: list[Area] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not set(self.area_type).issubset(set(PROJECT_TYPES)):
            raise ValueError("Area type must be of from predefined values.")
