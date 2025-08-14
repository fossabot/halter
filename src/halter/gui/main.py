from typing import Any

import flet as ft

from halter.core.constants import DEFAULT_PATH
from halter.core.models.project import Project
from halter.core.services.config_io import load_project


def main(page: ft.Page) -> None:
    page.title = "Halter - Network Planner"
    page.window_width = 1200
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE

    # Загружаем проект
    try:
        project: Project = load_project(DEFAULT_PATH)
    except Exception:
        project = Project(
            name="Новый проект", description="", area_type=["MNS"]
        )

    selected_view = ft.Ref[ft.Container]()

    def render_networks_table() -> Any:
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(n.name)),
                    ft.DataCell(ft.Text(n.address)),
                    ft.DataCell(ft.Text(str(n.vlan))),
                ]
            )
            for n in project.networks
        ]
        return ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Имя")),
                ft.DataColumn(label=ft.Text("IPv4")),
                ft.DataColumn(label=ft.Text("Маска")),
                ft.DataColumn(label=ft.Text("VLAN")),
            ],
            rows=rows,
        )

    def render_devices_table() -> Any:
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(d.name)),
                    ft.DataCell(ft.Text(d.role)),
                    ft.DataCell(ft.Text(str(len(d.interfaces)))),
                ]
            )
            for d in project.devices
        ]
        return ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Имя")),
                ft.DataColumn(label=ft.Text("Роль")),
                ft.DataColumn(label=ft.Text("Интерфейсов")),
            ],
            rows=rows,
        )

    def render_software_table() -> Any:
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(s.name)),
                    ft.DataCell(ft.Text(s.version)),
                ]
            )
            for s in project.software
        ]
        return ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Имя")),
                ft.DataColumn(label=ft.Text("Версия")),
                ft.DataColumn(label=ft.Text("Сеть")),
            ],
            rows=rows,
        )

    def on_drawer_change(e: ft.ControlEvent) -> None:
        label = e.control.controls[e.data].label
        if label == "Сети":
            content = render_networks_table()
        elif label == "Устройства":
            content = render_devices_table()
        elif label == "ПО":
            content = render_software_table()
        else:
            content = ft.Text(f"Раздел: {label}", size=20)
        selected_view.current.content = content
        page.update()

    drawer_controls = [
        ft.NavigationDrawerDestination(icon=ft.Icons.HOME, label="Проект"),
        ft.NavigationDrawerDestination(
            icon=ft.Icons.NETWORK_CELL, label="Сети"
        ),
        ft.NavigationDrawerDestination(
            icon=ft.Icons.DEVICES, label="Устройства"
        ),
        ft.NavigationDrawerDestination(icon=ft.Icons.SECURITY, label="ПО"),
        ft.NavigationDrawerDestination(
            icon=ft.Icons.SETTINGS, label="Настройки"
        ),
    ]

    page.drawer = ft.NavigationDrawer(
        controls=drawer_controls,
        on_change=on_drawer_change,
        on_dismiss=lambda _: None,
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Halter GUI"),
        leading=ft.IconButton(
            ft.Icons.MENU,
            on_click=lambda _: setattr(page.drawer, "open", True),
        ),
    )

    # Верхняя панель действий
    action_buttons = ft.Row(
        controls=[
            ft.OutlinedButton("Добавить", icon=ft.Icons.ADD),
            ft.OutlinedButton("Редактировать", icon=ft.Icons.EDIT),
            ft.OutlinedButton("Удалить", icon=ft.Icons.DELETE),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Центральная панель
    main_panel = ft.Container(
        ref=selected_view,
        expand=True,
        padding=20,
        content=ft.Text("Выберите раздел из меню."),
    )

    status_bar = ft.Container(
        content=ft.Text(f"Загружен проект: {project.name}", size=12),
        bgcolor=ft.Colors.BLUE_50,
        padding=10,
        alignment=ft.alignment.center_left,
    )

    page.add(
        ft.Column(
            [
                action_buttons,
                ft.Divider(),
                main_panel,
                ft.Divider(),
                status_bar,
            ]
        )
    )


def run() -> None:
    ft.app(target=main)
