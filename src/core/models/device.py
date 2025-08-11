from dataclasses import dataclass, field

from core.validation.validation import validate_netbios_name, validate_role

from .interface import NetworkInterface


@dataclass(slots=True, kw_only=True)
class Device:
    name: str  # NetBIOS
    description: str
    model: str
    role: str
    interfaces: list[NetworkInterface] = field(default_factory=list)
    software_used: list[str] = field(default_factory=list)
    firewall_id: str | None = None
    area_type: list[str] | None = None

    def __post_init__(self) -> None:
        validate_netbios_name(self.name)
        validate_role(self.role)
