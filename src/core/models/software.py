from dataclasses import dataclass, field
from enum import StrEnum

NETWORK_PROTOCOLS: list[str] = ["TCP", "UDP", "ICMP"]
NETWORK_DIRECTION: list[str] = ["inbound", "outbound", "io", "both"]


class Protocol(StrEnum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"


class Direction(StrEnum):
    In = "inbound"
    Out = "outbound"
    IO = "io"
    Both = "both"


@dataclass(slots=True, kw_only=True)
class Port:
    index: int
    description: str
    direction: Direction
    protocol: Protocol

    def __post_init__(self) -> None:
        if not (1 <= self.index <= 65535):
            raise ValueError(
                f"Port number must be between 1 and 65535, got {self.index}."
            )
        if self.direction not in NETWORK_DIRECTION:
            raise ValueError(
                f"Invalid direction: {self.direction!r}. Must be 'inbound', 'outbound', or 'io'."
            )

        if self.protocol not in NETWORK_PROTOCOLS:
            raise ValueError(
                f"Invalid protocol: {self.protocol!r}. Must be 'TCP' or 'UDP'."
            )


@dataclass(slots=True, kw_only=True)
class Software:
    name: str
    description: str
    version: str
    ports: list[Port] = field(default_factory=list)
