import flet as ft

from constants import APP_NAME
from network import build_network_container
from overview import build_overview_tab
from settings import SettingsContainer
from utils import emoji_str_cancat


class AppBar:
    def __init__(self, page: ft.Page, drawer: ft.NavigationDrawer) -> None:
        self.page: ft.Page = page
        self.drawer: ft.NavigationDrawer = drawer

        def open_drawer(e) -> None:
            self.drawer.open = True
            self.page.update()

        self.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.MENU,
                tooltip="Open navigation drawer",
                on_click=open_drawer,
            ),
            title=ft.Text(APP_NAME),
            center_title=True,
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="New", on_click=lambda e: print("New clicked")),
                        ft.PopupMenuItem(
                            text="Open",
                            on_click=lambda e: print("Open clicked"),
                        ),
                        ft.PopupMenuItem(
                            text="Save",
                            on_click=lambda e: print("Save clicked"),
                        ),
                        ft.PopupMenuItem(
                            text="Settings",
                            on_click=lambda e: print("Settings clicked"),
                        ),
                    ]
                )
            ],
        )


class AppNavigationDrawer:
    def __init__(self, page: ft.Page, container: ft.Container, views: list[ft.Control]) -> None:
        self.page: ft.Page = page
        self.container: ft.Container = container
        self.views: list[ft.Control] = views
        self.controls: list[ft.Control] = [
            ft.NavigationDrawerDestination(icon=ft.Icons.HOME, label="Overview"),
            ft.NavigationDrawerDestination(icon=ft.Icons.NETWORK_CELL, label="Network"),
            ft.NavigationDrawerDestination(icon=ft.Icons.SETTINGS, label="Settings"),
            ft.NavigationDrawerDestination(icon=ft.Icons.INFO, label="About"),
            ft.ElevatedButton(
                text="Add",
                icon=ft.Icons.ADD,
                on_click=self.on_add,
            ),
        ]
        self.nav_drawer = ft.NavigationDrawer(
            controls=self.controls,
            on_change=self.on_change,
            on_dismiss=self.on_dismiss,
        )

    def on_change(self, e: ft.ControlEvent) -> None:
        selected: int = e.control.selected_index  # index of destination

        if selected < len(self.views):
            self.container.content = self.views[selected]
        # close drawer
        self.nav_drawer.open = False
        self.page.appbar.title = ft.Text(  # type: ignore
            emoji_str_cancat(self.controls[selected].label)  # type: ignore
        )
        self.page.update()

    def on_dismiss(self, e: ft.ControlEvent) -> None:
        print("Drawer dismissed")

    def on_add(self, e: ft.ControlEvent) -> None:
        # Create new view and destination
        new_index: int = len(self.views)
        label: str = f"New {new_index}"
        new_view = ft.Column(
            [ft.Text(f"🔖 {label} Screen")],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
        self.views.append(new_view)
        new_dest = ft.NavigationDrawerDestination(
            icon=ft.Icons.LABEL,
            label=label,
        )
        # Insert before the Add button
        self.controls.insert(-1, new_dest)
        # Update drawer controls
        self.nav_drawer.controls = self.controls
        # Ensure newly added view shows when selected
        self.page.update()


if __name__ == "__main__":

    def main(page: ft.Page) -> None:
        page.title = APP_NAME
        # page.padding = 0
        page.theme = ft.Theme(font_family="Verdana")  # type: ignore
        page.theme_mode = ft.ThemeMode.SYSTEM

        # 1. prepare views
        overview: ft.Column = build_overview_tab(page)
        network: ft.Container = build_network_container(page)
        settings_view = SettingsContainer(page)
        about_view = ft.Column(
            [ft.Text("ℹ️ About Screen")],
            ft.MainAxisAlignment.CENTER,
            expand=True,
        )

        views: list[ft.Control] = [
            overview,
            network,
            settings_view,
            about_view,
        ]

        # 2. container for content
        content_container = ft.Container(content=overview, expand=True)

        # 3. navigation drawer with switching logic
        nav = AppNavigationDrawer(page, content_container, views)

        # 4. app bar with drawer toggle
        app_bar = AppBar(page, nav.nav_drawer)

        # 5. attach to page
        page.drawer = nav.nav_drawer
        page.appbar = app_bar.appbar
        page.add(content_container)

        page.update()

    ft.app(target=main)
