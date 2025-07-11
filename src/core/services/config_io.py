from dataclasses import fields, is_dataclass

import yaml

from core.models.device import Device
from core.models.interface import NetworkInterface
from core.models.network import Network
from core.models.project import Project
from core.models.software import Software


def save_project(project: Project, path: str) -> None:
    """Сериализует проект в YAML-файл с поддержкой слотов"""

    def to_dict(obj):
        """Рекурсивно преобразует объекты со слотами/датаклассы в словари"""
        if is_dataclass(obj):
            # Для датаклассов используем официальное API
            return {f.name: to_dict(getattr(obj, f.name)) for f in fields(obj)}
        elif hasattr(obj, "__slots__"):
            # Для обычных классов со слотами
            return {
                slot: to_dict(getattr(obj, slot)) for slot in obj.__slots__
            }
        elif isinstance(obj, list):
            return [to_dict(item) for item in obj]
        return obj

    data = to_dict(project)
    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False)


def load_project(path: str) -> Project:
    """Десериализует проект из YAML-файла"""
    with open(path) as f:
        data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError("YAML root must be a dictionary.")

    networks = [Network(**n) for n in data.get("networks", [])]

    devices = []
    for d in data.get("devices", []):
        interfaces = [NetworkInterface(**i) for i in d.get("interfaces", [])]
        # Создаем устройство, передавая все параметры из словаря
        device_params = {k: v for k, v in d.items() if k != "interfaces"}
        device_params["interfaces"] = interfaces
        devices.append(Device(**device_params))

    software = [Software(**s) for s in data.get("software", [])]

    return Project(
        name=data["name"],
        description=data["description"],
        area_type=data["area_type"],
        networks=networks,
        devices=devices,
        software=software,
    )
