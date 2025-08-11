# tests/test_network_model.py

import pytest

from core.models.address import AddressingType
from core.models.network import VLAN, Network, NetworkTier, NetworkTopology

# VLAN tests


@pytest.mark.parametrize("valid_id", [1, 100, 4094])
def test_vlan_valid_ids(valid_id: int) -> None:
    """VLAN accepts ids in the inclusive range 1–4094."""
    v = VLAN(id=valid_id, name="test")
    assert v.id == valid_id
    assert v.name == "test"


@pytest.mark.parametrize("invalid_id", [0, -1, 4095, 10000])
def test_vlan_invalid_ids(invalid_id: int) -> None:
    """VLAN rejects ids outside 1–4094."""
    with pytest.raises(ValueError) as exc:
        VLAN(id=invalid_id, name="bad")
    assert "VLAN id must be in [1, 4094]" in str(exc.value)


# Network tests


@pytest.fixture
def base_vlan() -> VLAN:
    return VLAN(id=10, name="vlan10")


@pytest.fixture
def base_network(base_vlan: VLAN) -> Network:
    """Create a valid Network instance using IPv4 network."""
    return Network(
        name="net1",
        description="Test network",
        vlan=base_vlan,
        topology=NetworkTopology.BUS,
        tier=NetworkTier.TIER_2,
        address_type=AddressingType.IP_NETWORK,
        address="192.168.0.0/24",
    )


def test_network_creation_with_valid_address(base_network: Network) -> None:
    """Network.__post_init__ should accept a valid address."""
    assert base_network.name == "net1"
    assert base_network.description == "Test network"
    assert base_network.vlan == base_network.vlan
    assert base_network.topology == NetworkTopology.BUS
    assert base_network.tier == NetworkTier.TIER_2
    assert base_network.address_type == AddressingType.IP_NETWORK
    assert base_network.address == "192.168.0.0/24"


def test_network_creation_with_invalid_address() -> None:
    """Invalid address on creation should raise ValueError."""
    with pytest.raises(ValueError):
        Network(
            name="badnet",
            description="/etet12&2123%",
            vlan=None,
            topology=NetworkTopology.MESH,
            tier=NetworkTier.TIER_1,
            address_type=AddressingType.IP_ADDRESS,
            address="999.999.999.999",
        )


def test_is_valid_address_true(base_network: Network) -> None:
    """is_valid_address() returns True for a valid address."""
    assert base_network.is_valid_address() is True


def test_is_valid_address_false(base_vlan: VLAN) -> None:
    """is_valid_address() returns False when address is changed to invalid."""
    # Сначала создаём с валидным HTTP URL
    net = Network(
        name="t",
        description="Test network",
        vlan=base_vlan,
        topology=NetworkTopology.PTP,
        tier=NetworkTier.TIER_0,
        address_type=AddressingType.HTTP_URL,
        address="http://example.com",
    )
    # Теперь присваиваем некорректный адрес и проверяем метод
    net.address = "invalid://url"
    assert net.is_valid_address() is False


def test_update_address_success(base_network: Network) -> None:
    """update_address() should change both address and type on success."""
    base_network.update_address("10.0.0.1", AddressingType.IP_ADDRESS)
    assert base_network.address == "10.0.0.1"
    assert base_network.address_type == AddressingType.IP_ADDRESS
    # original value_type change persists


def test_update_address_failure_reverts(base_network: Network) -> None:
    """On failure, update_address() must revert to old address and type."""
    old_addr = base_network.address
    old_type = base_network.address_type
    with pytest.raises(ValueError):
        base_network.update_address("not_an_ip", AddressingType.IP_ADDRESS)
    assert base_network.address == old_addr
    assert base_network.address_type == old_type


def test_get_address_type_name(base_network: Network) -> None:
    """get_address_type_name() returns the enum's .value string."""
    assert (
        base_network.get_address_type_name() == AddressingType.IP_NETWORK.value
    )
