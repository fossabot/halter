import ipaddress
from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class Network:
    name: str  # NetBIOS
    ipv4: str
    vlan: int

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
