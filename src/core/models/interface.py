import ipaddress
from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class NetworkInterface:
    number: int
    name: str
    network_id: str  # Will match Network.name
    ipv4: str
    routes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate_ipv4(self.ipv4)
        for route in self.routes:
            self._validate_ipv4(route)

    @staticmethod
    def _validate_ipv4(addr: str) -> None:
        try:
            ipaddress.ip_interface(addr)
        except ValueError as exc:
            raise ValueError(f"Invalid IPv4 address: {addr}") from exc
