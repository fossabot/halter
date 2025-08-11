# export_firewall.py
"""
Модуль для генерации конфигурационных файлов межсетевого экрана
"""

from pathlib import Path

from rich import print

from core.models.device import Device
from core.models.firewall import (
    Chain,
    FirewallConfig,
    FirewallRule,
    RuleAction,
)
from core.models.project import Project
from core.models.software import Port, Software


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
    current_ports: list[Port] = []
    for software_name in current_device.software_used:
        if software := software_map.get(software_name):
            current_ports.extend(software.ports)

    # Проверяем устройства на совпадение портов
    for other_device in devices:
        if other_device.name == current_device.name:
            continue

        # Получаем порты другого устройства
        other_ports: list[Port] = []
        for software_name in other_device.software_used:
            if software := software_map.get(software_name):
                other_ports.extend(software.ports)

        # Проверяем совпадение портов по индексу (номеру порта)
        current_set = set(port.index for port in current_ports)
        # print(f"{current_device.name}: Ports: {current_set}")
        other_set = set(port.index for port in other_ports)
        # print(f"{other_device.name}: Ports: {other_set}")
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
                    # Генерируем правила для софта с совпадающими портами
                    for software_name in current_device.software_used:
                        if software := software_map.get(software_name):
                            # Проверяем, есть ли порты этого софта с общими индексами
                            if any(
                                port.index in common_port_indices
                                for port in software.ports
                            ):
                                rules.extend(
                                    _generate_software_rules(
                                        software,
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


def _genereate_rules(
    current_sw: list[Software],
) -> list[FirewallRule]:
    return []


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


def _generate_software_rules(
    software: Software, ip_address: str, common_port_indices: set[int]
) -> list[FirewallRule]:
    """Генерирует правила для конкретного ПО с использованием мультипорт"""
    rules: list[FirewallRule] = []

    # Группируем порты по направлению и протоколу
    inbound_tcp_ports: list[int] = []
    inbound_udp_ports: list[int] = []
    outbound_tcp_ports: list[int] = []
    outbound_udp_ports: list[int] = []
    both_tcp_ports: list[int] = []
    both_udp_ports: list[int] = []

    for port in software.ports:
        if port.index in common_port_indices:
            if port.protocol.lower() == "tcp":
                if port.direction == "both":
                    both_tcp_ports.append(port.index)
                elif port.direction == "inbound":
                    inbound_tcp_ports.append(port.index)
                elif port.direction == "outbound":
                    outbound_tcp_ports.append(port.index)
            elif port.protocol.lower() == "udp":
                if port.direction == "both":
                    both_udp_ports.append(port.index)
                elif port.direction == "inbound":
                    inbound_udp_ports.append(port.index)
                elif port.direction == "outbound":
                    outbound_udp_ports.append(port.index)

    # Функция для создания мультипорт правил с учетом лимита в 15 портов
    def create_multiport_rules(
        chain: Chain, ports: list[int], protocol: str
    ) -> list[FirewallRule]:
        multiport_rules = []
        # Разбиваем на группы по 15 портов
        for i in range(0, len(ports), 15):
            port_group = ports[i : i + 15]
            if chain == Chain.INPUT:
                multiport_rules.append(
                    FirewallRule(
                        chain=chain,
                        action=RuleAction.ACCEPT,
                        protocol=protocol,
                        destination_ports=port_group,
                        source=ip_address,
                    )
                )
            else:
                multiport_rules.append(
                    FirewallRule(
                        chain=chain,
                        action=RuleAction.ACCEPT,
                        protocol=protocol,
                        source_ports=port_group,
                        destination=ip_address,
                    )
                )
        return multiport_rules

    # Создаем правила для TCP портов
    if inbound_tcp_ports:
        rules.extend(
            create_multiport_rules(Chain.INPUT, inbound_tcp_ports, "tcp")
        )

    if outbound_tcp_ports:
        rules.extend(
            create_multiport_rules(Chain.OUTPUT, outbound_tcp_ports, "tcp")
        )

    if both_tcp_ports:
        rules.extend(
            create_multiport_rules(Chain.INPUT, both_tcp_ports, "tcp")
        )
        rules.extend(
            create_multiport_rules(Chain.OUTPUT, both_tcp_ports, "tcp")
        )

    # Создаем правила для UDP портов
    if inbound_udp_ports:
        rules.extend(
            create_multiport_rules(Chain.INPUT, inbound_udp_ports, "udp")
        )

    if outbound_udp_ports:
        rules.extend(
            create_multiport_rules(Chain.OUTPUT, outbound_udp_ports, "udp")
        )

    if both_udp_ports:
        rules.extend(
            create_multiport_rules(Chain.INPUT, both_udp_ports, "udp")
        )
        rules.extend(
            create_multiport_rules(Chain.OUTPUT, both_udp_ports, "udp")
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
            "# Сохранить правила (раскомментируйте при необходимости)",
            "# iptables-save > /etc/iptables/rules.v4",
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
