import ipaddress
from dataclasses import dataclass
from enum import Enum


class AddressClass(Enum):
    A = 1
    B = 2
    C = 3


@dataclass(slots=True, kw_only=True)
class Network:
    name: str  # NetBIOS
    ipv4: str
    vlan: int
    address_class: AddressClass

    def __post_init__(self) -> None:
        if len(self.name) > 15:
            raise ValueError("NetBIOS name must be 15 characters or fewer.")
        self._validate_ipv4(self.ipv4)
        self._validate_ipv4(self.mask)
        if not (1 <= self.vlan <= 4094):
            raise ValueError("VLAN must be between 1 and 4094.")
        if self.address_class not in AddressClass:
            raise ValueError("Address class must be one of the A, B, C values")

    @staticmethod
    def _validate_ipv4(addr: str) -> None:
        try:
            ipaddress.ip_network(addr)

        except ValueError as exc:
            raise ValueError(f"Invalid IPv4 address: {addr}") from exc
