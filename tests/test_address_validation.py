# tests/test_address_validation.py
import pytest

from core.models.address import AddressingType
from core.models.network import VLAN, Network, NetworkTier, NetworkTopology
from core.validation.address_validators import (
    VALIDATION_FUNCTIONS,
)


# Parametrized test for pattern validators
@pytest.mark.parametrize(
    "atype, valid, invalid",
    [
        (
            AddressingType.OPC_UA_ADDRESS,
            ["opc.tcp://localhost:4840/service"],
            ["opc.tcp:/bad", "http://not.opc"],
        ),
        (
            AddressingType.DNS_NAME,
            ["example.com", "sub.domain.co"],
            [".example", "exa mple"],
        ),
        (
            AddressingType.HTTP_URL,
            ["http://test.local", "https://domain.com/path"],
            ["ftp://bad.url", "http//missing:"],
        ),
        (
            AddressingType.EMAIL_ADDRESS,
            ["user@example.com", "first.last@domain.co"],
            ["user@.com", "@no.local"],
        ),
    ],
)
def test_pattern_validators(atype, valid, invalid):
    func = VALIDATION_FUNCTIONS[atype]
    for addr in valid:
        assert func(addr) is None
    for addr in invalid:
        with pytest.raises(ValueError):
            func(addr)


# Test numeric validators
@pytest.mark.parametrize(
    "addr,ok",
    [("0", True), ("247", True), ("-1", False), ("248", False), ("a", False)],
)
def test_modbus_slaveid(addr, ok):
    func = VALIDATION_FUNCTIONS[AddressingType.MODBUS_RTU_ADDRESS]
    if ok:
        func(addr)
    else:
        with pytest.raises(ValueError):
            func(addr)


# Analog signals
@pytest.mark.parametrize(
    "sig,ok",
    [
        ("4-20mA", True),
        ("0-5V", True),
        ("100%", True),
        ("20mV", False),
        ("5-10", False),
    ],
)
def test_analog_signal(sig, ok):
    func = VALIDATION_FUNCTIONS[AddressingType.ANALOG_SIGNAL]
    if ok:
        func(sig)
    else:
        with pytest.raises(ValueError):
            func(sig)


# IP address and network
@pytest.mark.parametrize(
    "atype,addr,raises",
    [
        (AddressingType.IP_ADDRESS, "192.168.1.1", False),
        (AddressingType.IP_ADDRESS, "256.0.0.1", True),
        (AddressingType.IP_NETWORK, "10.0.0.0/24", False),
        (AddressingType.IP_NETWORK, "300.0.0.0/24", True),
    ],
)
def test_ip_address_network(atype, addr, raises):
    func = VALIDATION_FUNCTIONS[atype]
    if raises:
        with pytest.raises(ValueError):
            func(addr)
    else:
        func(addr)


# Database connection
@pytest.mark.parametrize(
    "conn,ok",
    [
        ("Server=my;Database=db", True),
        ("host=local;uid=1", True),
        ("justtext", False),
    ],
)
def test_database_connection(conn, ok):
    func = VALIDATION_FUNCTIONS[AddressingType.DATABASE_CONNECTION]
    if ok:
        func(conn)
    else:
        with pytest.raises(ValueError):
            func(conn)


# VLAN validation
def test_vlan_id_bounds():
    VLAN(id=1, name="A")
    VLAN(id=4094, name="B")
    for bad in [0, 4095, -1]:
        with pytest.raises(ValueError):
            VLAN(id=bad, name="X")


# Network class integration
@pytest.fixture
def base_network():
    return Network(
        name="net1",
        vlan=VLAN(id=10, name="net"),
        topology=NetworkTopology.BUS,
        tier=NetworkTier.TIER_2,
        address_type=AddressingType.IP_NETWORK,
        address="192.168.0.0/24",
    )


def test_network_valid_address(base_network):
    assert base_network.is_valid_address()


def test_network_invalid_address_on_creation():
    with pytest.raises(ValueError):
        Network(
            name="bad",
            vlan=None,
            topology=NetworkTopology.MESH,
            tier=NetworkTier.TIER_1,
            address_type=AddressingType.IP_ADDRESS,
            address="999.999.999.999",
        )


def test_update_address_success(base_network):
    base_network.update_address("10.0.0.1", AddressingType.IP_ADDRESS)
    assert base_network.address == "10.0.0.1"
    assert base_network.address_type == AddressingType.IP_ADDRESS


def test_update_address_failure_reverts(base_network):
    old_addr, old_type = base_network.address, base_network.address_type
    with pytest.raises(ValueError):
        base_network.update_address("bad.addr", AddressingType.IP_ADDRESS)
    assert base_network.address == old_addr
    assert base_network.address_type == old_type


# get_address_type_name
def test_get_address_type_name(base_network):
    assert (
        base_network.get_address_type_name() == AddressingType.IP_NETWORK.value
    )
