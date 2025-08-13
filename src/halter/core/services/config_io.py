# config_io.py
"""
Модуль для сохранения в yaml
"""

from dataclasses import fields, is_dataclass
from typing import Any

import yaml
from yaml import CSafeDumper as Dumper
from yaml import CSafeLoader as Loader

from halter.core.models.address import AddressingType
from halter.core.models.device import Device
from halter.core.models.interface import NetworkInterface
from halter.core.models.network import (
    VLAN,
    Network,
    NetworkTier,
    NetworkTopology,
)
from halter.core.models.project import Project
from halter.core.models.software import Port, Software


# Представитель для StrEnum: выводим просто строку
def _enum_representer(dumper: Any, obj: Any) -> Any:
    return dumper.represent_scalar("tag:yaml.org,2002:str", obj.value)


yaml.add_multi_representer(NetworkTopology, _enum_representer, Dumper=Dumper)
yaml.add_multi_representer(NetworkTier, _enum_representer, Dumper=Dumper)
yaml.add_multi_representer(AddressingType, _enum_representer, Dumper=Dumper)

# Преобразование любого объекта в примитивные структуры для dump


def to_dict(obj: Any) -> Any:
    if is_dataclass(obj):
        return {f.name: to_dict(getattr(obj, f.name)) for f in fields(obj)}
    elif hasattr(obj, "__slots__"):
        return {slot: to_dict(getattr(obj, slot)) for slot in obj.__slots__}
    elif isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj


def save_project(project: Project, path: str) -> None:
    """Сериализует Project в YAML без тегов классов"""
    data = to_dict(project)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, Dumper=Dumper, sort_keys=False, allow_unicode=True)


def load_project(path: str) -> Project:
    """Десериализует Project из YAML с учетом StrEnum"""
    with open(path, encoding="utf-8") as f:
        data = yaml.load(f, Loader=Loader)
    if not isinstance(data, dict):
        raise ValueError("YAML root must be mapping with Project fields.")

    # Сети
    try:
        nets = []
        for n in data.get("networks", []):
            n["topology"] = NetworkTopology(n["topology"])
            n["tier"] = NetworkTier(n["tier"])
            n["address_type"] = AddressingType(n["address_type"])
            if n["vlan"] is not None:
                n["vlan"] = VLAN(id=n["vlan"]["id"], name=n["vlan"]["name"])
            nets.append(Network(**n))
    except Exception as e:
        print(f"[red]Failed to load network {n}: [/red] {e}")

    # Устройства
    try:
        devs = []
        for d in data.get("devices", []):
            interfaces = [
                NetworkInterface(**i) for i in d.get("interfaces", [])
            ]
            params = {k: v for k, v in d.items() if k != "interfaces"}
            params["interfaces"] = interfaces
            devs.append(Device(**params))
    except Exception as e:
        print(f"[red]Failed to load device {d}: [/red] {e}")

    # ПО
    sws = []
    for s in data.get("software", []):
        ports = [Port(**p) for p in s.get("ports", [])]
        params = {k: v for k, v in s.items() if k != "ports"}
        params["ports"] = ports
        sws.append(Software(**params))

    return Project(
        name=data["name"],
        description=data["description"],
        area_type=data["area_type"],
        networks=nets,
        devices=devs,
        software=sws,
    )
