from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class Software:
    name: str
    description: str
    version: str
    has_network_capability: bool = False
    input_port: int | None = None
    output_port: int | None = None

    def __post_init__(self) -> None:
        if self.has_network_capability:
            if self.input_port is None or self.output_port is None:
                raise ValueError(
                    "Network-capable software must define both input and output ports."
                )
