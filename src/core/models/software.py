from dataclasses import dataclass, field

from core.constants import NETWORK_DIRECTION, NETWORK_PROTOCOLS


@dataclass(slots=True, kw_only=True)
class Port:
    index: int
    description: str
    direction: NETWORK_DIRECTION
    protocol: NETWORK_PROTOCOLS

    def __post_init__(self) -> None:
        if not (1 <= self.index <= 65535):
            raise ValueError(
                f"Port number must be between 1 and 65535, got {self.index}."
            )
        if self.direction not in {"inbound", "outbound", "io"}:
            raise ValueError(
                f"Invalid direction: {self.direction!r}. Must be 'inbound', 'outbound', or 'io'."
            )

        if self.protocol not in {"TCP", "UDP"}:
            raise ValueError(
                f"Invalid protocol: {self.protocol!r}. Must be 'TCP' or 'UDP'."
            )


@dataclass(slots=True, kw_only=True)
class Software:
    name: str
    description: str
    version: str
    ports: list[Port] = field(default_factory=list)
