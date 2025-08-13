# export_firewall.py
"""
Модуль для генерации конфигурационных файлов межсетевого экрана
"""

from pathlib import Path

from rich import print

from halter.core.models.device import Device
from halter.core.models.firewall import (
    Chain,
    FirewallConfig,
    FirewallRule,
    RuleAction,
)
from halter.core.models.project import Project
from halter.core.models.software import (
    NETWORK_DIRECTION,
    Direction,
    Port,
    Software,
)


def generate_firewall_config_for_device(
    current_device: Device,
    software_list: list[Software],
    devices: list[Device],
) -> FirewallConfig:
    """Генерирует конфигурацию фаервола для устройства на основе установленного ПО"""

    # Создаем маппинг software_name -> Software объект
    software_map = {sw.name: sw for sw in software_list}
    rules: list[FirewallRule] = []

    # Базовые правила
    rules.extend(_generate_security_rules())

    # Получаем порты текущего устройства
    current_ports: list[Port] = [
        port
        for software_name in current_device.software_used
        if (software := software_map.get(software_name))
        for port in software.ports
    ]

    # Проверяем устройства на совпадение портов
    for other_device in devices:
        if other_device.name == current_device.name or not (
            has_common_elements(
                current_device.area_type, other_device.area_type
            )
        ):
            continue

        # Получаем порты другого устройства
        other_ports: list[Port] = [
            port
            for software_name in other_device.software_used
            if (software := software_map.get(software_name))
            for port in software.ports
        ]

        # Проверяем совпадение портов по индексу (номеру порта)
        current_set = set(port.index for port in current_ports)
        other_set = set(port.index for port in other_ports)
        common_port_indices = current_set & other_set

        if not common_port_indices:
            continue

        # Находим общие сети
        for current_interface in current_device.interfaces:
            for other_interface in other_device.interfaces:
                if (
                    current_interface.network_id == other_interface.network_id
                    or current_interface.network_id in other_interface.routes
                ):
                    # Генерируем правила для совпадающих портов с правильными направлениями
                    rules.extend(
                        _generate_software_rules(
                            current_ports,
                            other_ports,
                            other_interface.address,
                            common_port_indices,
                        )
                    )
                    break  # Один раз для каждой сети

    rules.extend(_generate_final_rules())
    return FirewallConfig(
        rules=rules,
        default_policy_input=RuleAction.DROP,
        default_policy_forward=RuleAction.DROP,
        default_policy_output=RuleAction.DROP,
    )


def _generate_software_rules(
    current_ports: list[Port],
    other_ports: list[Port],
    other_address: str,
    common_port_indices: set[int],
) -> list[FirewallRule]:
    """Генерирует правила фаервола для портов с совпадающими индексами и направлениями"""

    rules: list[FirewallRule] = []

    # Создаем словари для быстрого поиска портов по индексу
    current_ports_by_index = create_unique_ports_with_right_direction(
        current_ports
    )
    other_ports_by_index = create_unique_ports_with_right_direction(
        other_ports
    )

    # Группируем порты по направлению и протоколу для текущего устройства
    inbound_tcp_ports: list[int] = []
    inbound_udp_ports: list[int] = []
    outbound_tcp_ports: list[int] = []
    outbound_udp_ports: list[int] = []

    try:
        for index in common_port_indices:
            current_port: Port = current_ports_by_index[index]
            other_port: Port = other_ports_by_index[index]

            # Проверяем совместимость направлений
            if _are_directions_compatible(
                current_port.direction, other_port.direction
            ):
                # Определяем реальное направление для текущего устройства
                actual_direction = _get_actual_direction(
                    current_port.direction, other_port.direction
                )
                if (
                    actual_direction == "both"
                    and current_port.protocol == "TCP"
                ):
                    inbound_tcp_ports.append(index)
                    outbound_tcp_ports.append(index)
                elif (
                    actual_direction == "both"
                    and current_port.protocol == "UDP"
                ):
                    inbound_udp_ports.append(index)
                    outbound_udp_ports.append(index)
                elif (
                    actual_direction == "inbound"
                    and current_port.protocol == "TCP"
                ):
                    inbound_tcp_ports.append(index)
                elif (
                    actual_direction == "inbound"
                    and current_port.protocol == "UDP"
                ):
                    inbound_udp_ports.append(index)
                elif (
                    actual_direction == "outbound"
                    and current_port.protocol == "TCP"
                ):
                    outbound_tcp_ports.append(index)
                elif (
                    actual_direction == "outbound"
                    and current_port.protocol == "UDP"
                ):
                    outbound_udp_ports.append(index)
    except Exception as e:
        print(f"[red]Failed! Port index is {index} [/red] {e}")

    # Функция для создания мультипорт правил с учетом лимита в 15 портов
    def create_multiport_rules(
        chain: Chain, ports: list[int], protocol: str
    ) -> list[FirewallRule]:
        multiport_rules = []
        # Разбиваем на группы по 15 портов
        # print(f"{len(ports)}")
        for i in range(0, len(ports), 15):
            port_group = ports[i : i + 15]
            if chain == Chain.INPUT:
                multiport_rules.append(
                    FirewallRule(
                        chain=chain,
                        action=RuleAction.ACCEPT,
                        protocol=protocol,
                        destination_ports=port_group,
                        source=other_address,
                    )
                )
            else:
                multiport_rules.append(
                    FirewallRule(
                        chain=chain,
                        action=RuleAction.ACCEPT,
                        protocol=protocol,
                        source_ports=port_group,
                        destination=other_address,
                    )
                )
        return multiport_rules

    # Создаем правила для TCP портов
    if inbound_tcp_ports:
        rules.extend(
            create_multiport_rules(
                Chain.INPUT, sorted(inbound_tcp_ports), "tcp"
            )
        )

    # Создаем правила для UDP портов
    if inbound_udp_ports:
        rules.extend(
            create_multiport_rules(
                Chain.INPUT, sorted(inbound_udp_ports), "udp"
            )
        )

    if outbound_tcp_ports:
        rules.extend(
            create_multiport_rules(
                Chain.OUTPUT, sorted(outbound_tcp_ports), "tcp"
            )
        )
    if outbound_udp_ports:
        rules.extend(
            create_multiport_rules(
                Chain.OUTPUT, sorted(outbound_udp_ports), "udp"
            )
        )

    return rules


def _are_directions_compatible(dir1: Direction, dir2: Direction) -> bool:
    """Проверяет совместимость направлений для соединения двух устройств.

    Args:
        dir1: Направление первого устройства
        dir2: Направление второго устройства

    Returns:
        True - если направления совместимы (может быть установлено соединение)
        False - если направления несовместимы (соединение невозможно)

    Правила:
        - Both совместим с любым направлением (In, Out, Both)
        - In совместим только с Out или Both
        - Out совместим только с In или Both
        - In+In и Out+Out - несовместимые комбинации
    """
    # Обрабатываем случай, когда хотя бы одно устройство работает в обоих направлениях
    if Direction.Both in (dir1, dir2):
        return True

    # Проверяем взаимно совместимые комбинации
    return (dir1 == Direction.In and dir2 == Direction.Out) or (
        dir1 == Direction.Out and dir2 == Direction.In
    )


def _generate_final_rules() -> list[FirewallRule]:
    """Генерирует финальные правила"""
    return [
        # Блокировка SSH по умолчанию
        FirewallRule(
            chain=Chain.INPUT,
            action=RuleAction.DROP,
            protocol="tcp",
            destination_ports=[22],
        ),
    ]


def _generate_security_rules() -> list[FirewallRule]:
    """Генерирует базовые правила безопасности"""
    rules: list[FirewallRule] = []

    # Разрешить loopback
    rules.extend(
        [
            FirewallRule(
                chain=Chain.INPUT, action=RuleAction.ACCEPT, interface_in="lo"
            ),
            FirewallRule(
                chain=Chain.OUTPUT,
                action=RuleAction.ACCEPT,
                interface_out="lo",
            ),
        ]
    )

    # Разрешить ICMP
    rules.extend(
        [
            FirewallRule(
                chain=Chain.INPUT,
                action=RuleAction.ACCEPT,
                protocol="icmp",
                icmp_type="echo-reply",
            ),
            FirewallRule(
                chain=Chain.INPUT,
                action=RuleAction.DROP,
                protocol="icmp",
                icmp_type="destination-unreachable",
            ),
            FirewallRule(
                chain=Chain.INPUT,
                action=RuleAction.DROP,
                protocol="icmp",
                icmp_type="time-exceeded",
            ),
            FirewallRule(
                chain=Chain.INPUT,
                action=RuleAction.ACCEPT,
                protocol="icmp",
                icmp_type="echo-request",
            ),
            FirewallRule(
                chain=Chain.OUTPUT, action=RuleAction.ACCEPT, protocol="icmp"
            ),
        ]
    )

    # Разрешить established/related соединения
    rules.extend(
        [
            FirewallRule(
                chain=Chain.INPUT,
                action=RuleAction.ACCEPT,
                protocol="all",
                state="ESTABLISHED,RELATED",
                state_match=True,
            ),
            FirewallRule(
                chain=Chain.OUTPUT,
                action=RuleAction.ACCEPT,
                protocol="all",
                state="ESTABLISHED,RELATED",
                state_match=True,
            ),
            FirewallRule(
                chain=Chain.FORWARD,
                action=RuleAction.ACCEPT,
                protocol="all",
                state="ESTABLISHED,RELATED",
                state_match=True,
            ),
        ]
    )

    # Защита от атак
    rules.extend(
        [
            FirewallRule(
                chain=Chain.INPUT, action=RuleAction.DROP, state="INVALID"
            ),
            FirewallRule(
                chain=Chain.FORWARD, action=RuleAction.DROP, state="INVALID"
            ),
            FirewallRule(
                chain=Chain.INPUT,
                action=RuleAction.DROP,
                protocol="tcp",
                tcp_flags="--tcp-flags ALL NONE",
            ),
            FirewallRule(
                chain=Chain.INPUT,
                action=RuleAction.DROP,
                protocol="tcp",
                tcp_flags="! --syn",
                state="NEW",
            ),
            FirewallRule(
                chain=Chain.OUTPUT,
                action=RuleAction.DROP,
                protocol="tcp",
                tcp_flags="! --syn",
                state="NEW",
            ),
        ]
    )

    return rules


def export_firewall_configs(project: Project, output_dir: Path) -> None:
    # Создаём путь: отдельная папка для проекта
    project_dir = output_dir / project.name
    project_dir.mkdir(parents=True, exist_ok=True)

    for device in project.devices:
        # Поддиректория для устройства
        device_dir = project_dir / device.name
        device_dir.mkdir(parents=True, exist_ok=True)

        # Экспорт конфигурации
        export_firewall_config_of_device(
            device, project.software, device_dir, project.devices
        )


def export_firewall_config_of_device(
    device: Device,
    software: list[Software],
    output_dir: Path,
    devices: list[Device],
) -> None:
    """Экспортирует конфигурации фаервола в файлы"""

    # Генерируем конфигурацию
    fw_config = generate_firewall_config_for_device(device, software, devices)

    # Генерируем скрипт
    if device.firewall_id == "iptables":
        iptables_script = generate_iptables_script(fw_config)
        (output_dir / "iptables.sh").write_text(
            iptables_script, encoding="utf-8"
        )

        print(
            f"[green]Firewall (iptables) config saved to {output_dir}[/green]"
        )


def generate_iptables_script(config: FirewallConfig) -> str:
    """Генерирует bash-скрипт для настройки iptables"""
    lines: list[str] = []

    # Шебанг и заголовок
    lines.extend(
        [
            "#!/bin/bash",
            "# Проверяем, есть ли у пользователя права суперпользователя",
            "if [[ $EUID -ne 0 ]]; then",
            "    echo 'Этот скрипт должен быть запущен c правами администратора' ",
            "    exit 1",
            "fi",
            "",
            "iptables -F",
            "iptables -F -t nat",
            "iptables -F -t mangle",
            "iptables -X",
            "iptables -t nat -X",
            "iptables -t mangle -X",
            "",
            f"iptables -P INPUT {config.default_policy_input.value}",
            f"iptables -P OUTPUT {config.default_policy_output.value}",
            f"iptables -P FORWARD {config.default_policy_forward.value}",
            "",
        ]
    )

    # Добавляем пользовательские правила
    for rule in config.rules:
        lines.append(_generate_rule(rule))

    # Сохранить правила (опционально)
    lines.extend(
        [
            "",
            "# Создаем файл iptables в каталоге if-pre-up.d",
            "# Настройка автоматического восстановления iptables правил при загрузке",
            "mkdir -p /etc/network/if-pre-up.d",
            "echo '#!/bin/sh' | sudo tee /etc/network/if-pre-up.d/iptables",
            "echo 'iptables-restore < /etc/iptables.rules' | tee -a /etc/network/if-pre-up.d/iptables",
            "echo 'exit 0' | tee -a /etc/network/if-pre-up.d/iptables",
            "chmod +x /etc/network/if-pre-up.d/iptables",
            "",
            "# Сохранить правила",
            "/sbin/iptables-save > /etc/iptables.rules",
            "",
            "# Проверить результат",
            "# ls -la /etc/network/if-pre-up.d/iptables",
        ]
    )

    return "\n".join(lines)


def _generate_rule(rule: FirewallRule) -> str:
    """Генерирует одну строку iptables правила"""
    cmd_parts = ["iptables"]

    # Команда и цепочка
    cmd_parts.extend(["-A", rule.chain.value])

    # Протокол
    if rule.protocol:
        cmd_parts.extend(["-p", rule.protocol])
    elif rule.destination_ports or rule.source_ports:
        cmd_parts.extend(["-p", "tcp"])

    if hasattr(rule, "tcp_flags") and rule.tcp_flags:
        cmd_parts.extend([rule.tcp_flags])

    if hasattr(rule, "state") and rule.state:
        cmd_parts.extend(["-m state", "--state", rule.state])

    if hasattr(rule, "icmp_type") and rule.icmp_type:
        cmd_parts.extend(["--icmp-type", rule.icmp_type])

    # Интерфейсы
    if rule.interface_in:
        cmd_parts.extend(["-i", rule.interface_in])
    if rule.interface_out:
        cmd_parts.extend(["-o", rule.interface_out])

    # Порты destination_ports
    if rule.source_ports:
        if len(rule.source_ports) == 1:
            cmd_parts.extend(
                ["--sport", ports_to_multi_or_single(rule.source_ports)]
            )
        elif len(rule.source_ports) > 1:
            cmd_parts.extend(
                [
                    "--match multiport --sports",
                    ports_to_multi_or_single(rule.source_ports),
                ]
            )
    if rule.destination_ports:
        if len(rule.destination_ports) == 1:
            cmd_parts.extend(
                ["--dport", ports_to_multi_or_single(rule.destination_ports)]
            )
        elif len(rule.destination_ports) > 1:
            cmd_parts.extend(
                [
                    "--match multiport --dports",
                    ports_to_multi_or_single(rule.destination_ports),
                ]
            )

    # Адреса
    if rule.source:
        cmd_parts.extend(["-s", rule.source])
    if rule.destination:
        cmd_parts.extend(["-d", rule.destination])

    # Действие

    cmd_parts.extend(["-j", rule.action.value])

    return " ".join(cmd_parts)


def ports_to_multi_or_single(ports: list[int]) -> str:
    return ", ".join(map(str, ports))


def _get_actual_direction(
    current_direction: Direction, other_direction: Direction
) -> NETWORK_DIRECTION:
    """Определяет реальное направление трафика для текущего устройства с учетом направления другого устройства.

    Использует pattern matching (PEP 634) и Literal типы для лучшей типобезопасности.

    Args:
        current_direction: Направление текущего устройства
        other_direction: Направление другого устройства

    Returns:
        "inbound" - для входящего трафика
        "outbound" - для исходящего трафика
        "both" - для обоих направлений

    Raises:
        ValueError: При несовместимых направлениях (In+In или Out+Out)
    """
    match (current_direction, other_direction):
        # Оба устройства работают в двух направлениях
        case (Direction.Both, Direction.Both):
            return "both"

        # Текущее устройство - Both
        case (Direction.Both, Direction.In):
            return "outbound"
        case (Direction.Both, Direction.Out):
            return "inbound"

        # Другое устройство - Both
        case (Direction.In, Direction.Both):
            return "inbound"
        case (Direction.Out, Direction.Both):
            return "outbound"

        # Стандартные совместимые случаи
        case (Direction.In, Direction.Out):
            return "inbound"
        case (Direction.Out, Direction.In):
            return "outbound"

        # Некорректные комбинации
        case (Direction.In, Direction.In):
            raise ValueError("Incompatible directions: In+In")
        case (Direction.Out, Direction.Out):
            raise ValueError("Incompatible directions: Out+Out")

        # Все остальные случаи (для полноты)
        case _:
            return "both"


def create_unique_ports_with_right_direction(
    ports: list[Port],
) -> dict[int, Port]:
    """
    Создает словарь портов с высшим направлнием:
    если есть оба направления, выбирается both
    """
    port_dict: dict[int, Port] = {}

    for port in ports:
        if port.index not in port_dict:
            port_dict[port.index] = port
        else:
            # Если уже есть порт с таким индексом, проверяем приоритет
            existing_port = port_dict[port.index]
            # Если новый или существующий порт имеет направление both, выбираем его
            if (
                port.direction == Direction.Both
                or existing_port.direction == Direction.Both
            ):
                # Оставляем порт с направлением both
                if port.direction == Direction.Both:
                    port_dict[port.index] = port
            # Если оба порта inbound/outbound, можно оставить любой или объединить логику
            # В данном случае оставляем существующий

    return port_dict


def has_common_elements(list1: list[str], list2: list[str]) -> bool:
    """
    Проверяет, есть ли общие элементы в двух списках
    (для чисел, кортежей и других хешируемых типов).
    """
    return any(item in list2 for item in list1)
