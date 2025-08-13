# test_network_config.py

import pytest

from halter.core.models.address import AddressingType
from halter.core.models.device import Device
from halter.core.models.interface import NetworkInterface, VlanMode
from halter.core.models.network import (
    VLAN,
    Network,
    NetworkTier,
    NetworkTopology,
)
from halter.core.services.export.network_config import (
    EXPORT_HANDLERS,
    export_interface_configs_of_device,
    export_linux_networking,
    export_regul_networking,
    register_handler,
)

# === Тестовые данные ===


@pytest.fixture
def sample_networks() -> list[Network]:
    return [
        Network(
            name="SomeHMI_OSN",
            description="",
            topology=NetworkTopology("Star"),
            tier=NetworkTier("SCADA and HMI"),
            address_type=AddressingType("IPv4 Network"),
            vlan=VLAN(id=999, name="HMI"),
            address="192.168.133.0/28",
            gateway="192.168.133.3",
        ),
        Network(
            name="SomeHMI_REZ",
            description="",
            vlan=VLAN(id=666, name="PLC"),
            address="192.168.133.128/28",
            gateway="192.168.133.131",
            topology=NetworkTopology("Star"),
            tier=NetworkTier("Controllers"),
            address_type=AddressingType("IPv4 Network"),
        ),
        Network(
            name="SomeARM_OSN",
            description="",
            topology=NetworkTopology("Star"),
            tier=NetworkTier("SCADA and HMI"),
            address_type=AddressingType("IPv4 Network"),
            vlan=VLAN(id=999, name="HMI"),
            address="192.168.133.16/28",
            gateway="192.168.133.18",
        ),
        Network(
            name="SomeARM_REZ",
            description="",
            vlan=VLAN(id=666, name="PLC"),
            address="192.168.133.144/28",
            gateway="192.168.133.146",
            topology=NetworkTopology("Star"),
            tier=NetworkTier("Controllers"),
            address_type=AddressingType("IPv4 Network"),
        ),
    ]


@pytest.fixture
def sample_device() -> Device:
    return Device(
        name="AMNS-CK-TEST-S",
        description="АРМ Оператора Тест",
        model="IROBO",
        role="Workstation",
        interfaces=[
            NetworkInterface(
                name="eth4",
                network_id="SomeHMI_OSN",
                routes=["SomeARM_OSN"],
                address_type=AddressingType("IPv4 Address"),
                address="192.168.133.4",
                vlan_mode=VlanMode.ACCESS,
                software_id="networking",
            ),
            NetworkInterface(
                name="eth0",
                network_id="SomeHMI_REZ",
                routes=["SomeARM_REZ"],
                address_type=AddressingType("IPv4 Address"),
                address="192.168.133.132",
                vlan_mode=VlanMode.ACCESS,
                software_id="networking",
            ),
        ],
    )


# === Тесты для обработчиков ===


def test_export_linux_networking(sample_networks: list[Network]) -> None:
    network_map = {net.name: net for net in sample_networks}
    device = Device(
        name="TestDevice",
        description="",
        model="",
        role="Workstation",
        interfaces=[
            NetworkInterface(
                name="eth0",
                network_id="SomeHMI_OSN",
                routes=["SomeARM_OSN"],
                address_type=AddressingType("IPv4 Address"),
                address="192.168.133.5",
                vlan_mode=VlanMode.ACCESS,
                software_id="networking",
            )
        ],
    )

    result = export_linux_networking(device, network_map)
    config = result["interfaces"]

    assert "auto eth0" in config
    assert "address 192.168.133.5" in config
    assert (
        "up ip route add 192.168.133.16/28 via 192.168.133.3 dev eth0"
        in config
    )


def test_export_regul_networking(sample_networks: list[Network]) -> None:
    network_map = {net.name: net for net in sample_networks}
    device = Device(
        name="PLC-TEst-A",
        description="",
        model="",
        role="PLC",
        interfaces=[
            NetworkInterface(
                name="port30",
                network_id="SomeHMI_OSN",
                routes=["SomeARM_OSN"],
                address_type=AddressingType("IPv4 Address"),
                address="192.168.133.5",
                vlan_mode=VlanMode.ACCESS,
                software_id="regul_networking",
            )
        ],
    )

    result = export_regul_networking(device, network_map)
    network_cfg = result["network.cfg"]
    routes = result["routes"]

    assert "[global]" in network_cfg
    assert "hostname=PLC-TEst-A" in network_cfg
    assert "port30=192.168.133.5 255.255.255.240" in network_cfg
    assert "-net 192.168.133.16/28 192.168.133.3" in routes


# === Интеграционный тест ===


def test_export_interface_configs_of_device(
    sample_device: Device, sample_networks: list[Network]
) -> None:
    configs = export_interface_configs_of_device(
        sample_device, sample_networks
    )

    assert "interfaces" in configs
    content = configs["interfaces"]

    # Проверим, что маршруты добавлены
    assert (
        "up ip route add 192.168.133.16/28 via 192.168.133.3 dev eth4"
        in content
    )
    assert (
        "up ip route add 192.168.133.144/28 via 192.168.133.131 dev eth0"
        in content
    )

    # Проверим, что интерфейсы настроены
    assert "auto eth4" in content
    assert "address 192.168.133.4" in content
    assert "address 192.168.133.132" in content


# === Тест ошибок ===


def test_missing_network_raises_error(sample_networks: list[Network]) -> None:
    network_map = {net.name: net for net in sample_networks}
    device = Device(
        name="TestDevice",
        description="",
        model="",
        role="Workstation",
        interfaces=[
            NetworkInterface(
                name="eth0",
                network_id="NONEXISTENT",
                routes=[],
                address_type=AddressingType("IPv4 Address"),
                address="192.168.1.1",
                vlan_mode=VlanMode.ACCESS,
                software_id="networking",
            )
        ],
    )

    with pytest.raises(ValueError, match="No network found"):
        export_linux_networking(device, network_map)


# === Тест регистрации обработчиков ===


def test_register_handler() -> None:
    def dummy_handler(
        device: Device, network_map: dict[str, Network]
    ) -> dict[str, str]:
        return {"dummy": "config"}

    register_handler("dummy_software")(dummy_handler)

    assert "dummy_software" in EXPORT_HANDLERS
    assert EXPORT_HANDLERS["dummy_software"] is dummy_handler
