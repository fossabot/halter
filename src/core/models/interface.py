from dataclasses import dataclass, field
from enum import StrEnum

from core.models.address import AddressingType
from core.validation.address_validators import VALIDATION_FUNCTIONS


class VlanMode(StrEnum):
    ACCESS = "Access"
    TRUNK = "Trunk"
    HYBRID = "Hybrid"


@dataclass(slots=True, kw_only=True)
class NetworkInterface:
    name: str
    network_id: str  # Will match Network.name
    routes: list[str] = field(default_factory=list)
    address_type: AddressingType
    address: str
    vlan_mode: VlanMode
    software_id: str

    def __post_init__(self) -> None:
        self._validate_address()

    def _validate_address(self) -> None:
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
