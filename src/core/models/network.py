# core/models/network.py
from dataclasses import dataclass
from enum import StrEnum

from core.models.address import AddressingType
from core.validation.address_validators import VALIDATION_FUNCTIONS


class NetworkTier(StrEnum):
    TIER_0 = "Field Devices"
    TIER_1 = "I/O and Distributed Controllers"
    TIER_2 = "Controllers"
    TIER_3 = "SCADA and HMI"
    TIER_4 = "MES Level"
    TIER_5 = "Enterprise Level"


class NetworkTopology(StrEnum):
    PTP = "Point-to-Point"
    BUS = "Bus"
    D_BUS = "Duplicated Bus"
    STAR = "Star"
    RING = "Ring"
    R_RING = "Redundant Ring"
    MESH = "Mesh"
    FC_MESH = "Fully Connected Mesh"
    PC_MESH = "Partially Connected Mesh"
    TREE = "Tree"


@dataclass(slots=True, kw_only=True)
class VLAN:
    id: int
    name: str

    def __post_init__(self) -> None:
        if not 1 <= self.id <= 4094:
            raise ValueError("VLAN id must be in [1, 4094]")


@dataclass(slots=True, kw_only=True)
class Network:
    name: str
    vlan: VLAN | None = None
    topology: NetworkTopology
    tier: NetworkTier
    address_type: AddressingType
    address: str | None = None
    gateway: str | None = None

    def __post_init__(self) -> None:
        self._validate_address()

    def _validate_address(self) -> None:
        if self.address is not None:
            if validator := VALIDATION_FUNCTIONS.get(self.address_type):
                validator(self.address)

    def update_address(
        self,
        new_address: str,
        new_address_type: AddressingType | None = None,
    ) -> None:
        old_type, old_addr = self.address_type, self.address
        try:
            if new_address_type:
                self.address_type = new_address_type
            self.address = new_address
            self._validate_address()
        except Exception:
            self.address_type, self.address = old_type, old_addr
            raise

    def is_valid_address(self) -> bool:
        try:
            self._validate_address()
            return True
        except ValueError:
            return False

    def get_address_type_name(self) -> str:
        return self.address_type.value
