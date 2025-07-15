import ipaddress
from dataclasses import dataclass
from enum import Enum

from core.constants import NETWORK_ZONE


class NetworkTier(Enum):
    ACCESS = "access"
    DISTRIBUTION = "distribution"
    CORE = "core"


class NetworkTopology(Enum):
    TRUSTED = "trusted"
    DMZ = "dmz"
    IOT = "iot"
    GUEST = "guest"


@dataclass(slots=True, kw_only=True)
class VLAN:
    id: int = 1
    name: str
    purpose: str | None = None
    zone: NETWORK_ZONE

    def __post_init__(self) -> None:
        if not (1 <= self.id <= 4094):
            raise ValueError("VLAN must be between 1 and 4094.")


@dataclass(slots=True, kw_only=True)
class Network:
    name: str  # NetBIOS
    ipv4: str  # ip адрес плюс маска (/28)
    vlan: VLAN
    topology: NetworkTopology

    def __post_init__(self) -> None:
        if len(self.name) > 15:
            raise ValueError("NetBIOS name must be 15 characters or fewer.")
        self._validate_ipv4(self.ipv4)
        if not (1 <= self.vlan <= 4094):
            raise ValueError("VLAN must be between 1 and 4094.")

    @staticmethod
    def _validate_ipv4(addr: str) -> None:
        try:
            ipaddress.ip_network(addr)

        except ValueError as exc:
            raise ValueError(f"Invalid IPv4 network address: {addr}") from exc
