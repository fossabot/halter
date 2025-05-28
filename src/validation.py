import ipaddress
import re
from enum import Enum

import flet as ft


class ValidationType(Enum):
    NotEmpty = 1
    OnlyEnglish = 2
    NotSelected = 3
    IPv4HostAddress = 4
    IPv4NetworkAddress = 5
    VLAN = 6


class InputValidator:
    def __init__(self, page: ft.Page) -> None:
        self.page: ft.Page = page

    def validate(
        self,
        validation_type: ValidationType,
        event: ft.ControlEvent,
        parameter: str | None = None,
        parameter2: str | None = None,
    ) -> bool:
        if validation_type == ValidationType.NotEmpty:
            return self._validate_not_empty(event)
        elif validation_type == ValidationType.OnlyEnglish:
            return self._validate_english_name(event)
        elif validation_type == ValidationType.NotSelected:
            return self._validate_dropdown(event)
        elif validation_type == ValidationType.IPv4HostAddress:
            return self._validate_ipv4_host(event, parameter, parameter2)
        elif validation_type == ValidationType.IPv4NetworkAddress:
            return self._validate_ipv4_network(event, parameter)
        elif validation_type == ValidationType.VLAN:
            return self._validate_vlan_id(event)

    def _validate_vlan_id(self, e: ft.ControlEvent) -> bool:
        try:
            vlan_id = int(e.control.value)
            if 1 <= vlan_id <= 4095:
                return True
            else:
                self._show_error("VLAN must be between 1 and 4095.")
                return False
        except (ValueError, TypeError):
            self._show_error("VLAN must be a number between 1 and 4095.")
            return False

    def _validate_not_empty(self, e: ft.ControlEvent) -> bool:
        if not e.control.value:
            self._show_error("Field cannot be empty.")
            return False
        return True

    def _validate_english_name(self, e: ft.ControlEvent) -> bool:
        if not e.control.value:
            self._show_error("English name cannot be empty.")
            return False
        if not re.match(r"^[a-zA-Z0-9_\- ]+$", e.control.value):
            self._show_error(
                "English name must contain only Latin letters, numbers, spaces, dashes or underscores."
            )
            return False
        return True

    def _validate_dropdown(self, e: ft.ControlEvent) -> bool:
        if not e.control.value:
            self._show_error(f"Please select a value for '{e.control.label}'.")
            return False
        return True

    def _validate_ipv4_network(self, e: ft.ControlEvent, mask) -> bool:
        try:
            ip_str: str = e.control.value.strip()
            network = ipaddress.IPv4Network(f"{ip_str}/{mask}", strict=True)
            if network.network_address.exploded != ip_str:
                self._show_error("This IP is not a valid network address.")
                return False
            return True
        except Exception:
            self._show_error("Invalid IPv4 network address.")
            return False

    def _validate_ipv4_host(self, e: ft.ControlEvent, mask, network_ip) -> bool:
        try:
            ip_str: str = e.control.value.strip()
            network = ipaddress.IPv4Network(f"{network_ip}/{mask}", strict=False)
            ip = ipaddress.IPv4Address(ip_str)

            if ip == network.network_address or ip == network.broadcast_address:
                self._show_error("This IP cannot be a network or broadcast address.")
                return False
            if ip not in network:
                self._show_error("This IP is not in the specified subnet.")
                return False
            return True
        except Exception:
            self._show_error("Invalid IPv4 host address.")
            return False

    def _show_error(self, message: str) -> None:
        self.page.open(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED_500,
                action="OK",
                duration=2000,
            )
        )
        self.page.update()
