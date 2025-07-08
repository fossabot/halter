import flet as ft

from validation import InputValidator


class SettingsContainer(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.validator = InputValidator(page)
        self.expand = True
        self.padding = 20
        self.content = self.build_content()

    def build_content(self) -> ft.Column:
        # Window Settings
        self.fullscreen_switch = ft.Switch(
            label="Fullscreen",
            value=self.page.window.full_screen,
            on_change=self.toggle_fullscreen,
        )

        self.resizable_switch = ft.Switch(
            label="Resizable Window",
            value=self.page.window.resizable,
            on_change=self.toggle_resizable,
        )

        self.width_field = ft.TextField(
            label="Window Width",
            value=str(self.page.window.width),
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.update_window_width,
        )

        self.height_field = ft.TextField(
            label="Window Height",
            value=str(self.page.window.height),
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.update_window_height,
        )

        self.theme_changer = ft.Dropdown(
            label="Theme",
            options=[
                ft.dropdown.Option(c)
                for c in [
                    "LIGHT",
                    "DARK",
                    "SYSTEM",
                ]
            ],
            on_change=self.change_theme,
            width=300,
        )

        return ft.Column(
            [
                ft.Text("🪟 Window Settings", size=20, weight=ft.FontWeight.W_600),
                self.theme_changer,
                self.fullscreen_switch,
                self.resizable_switch,
                ft.Row([self.width_field, self.height_field]),
                ft.Divider(),
                ft.Text("🎨 Color Settings", size=20, weight=ft.FontWeight.W_600),
            ],
            spacing=15,
        )

    def change_theme(self, e: ft.ControlEvent) -> None:
        if e.control.value == "LIGHT":
            self.page.theme_mode = ft.ThemeMode.LIGHT
        elif e.control.value == "DARK":
            self.page.theme_mode = ft.ThemeMode.DARK
        elif e.control.value == "SYSTEM":
            self.page.theme_mode = ft.ThemeMode.SYSTEM
        self._notify(f"Theme changed to {e.control.value}")
        self.page.update()

    def toggle_fullscreen(self, e: ft.ControlEvent) -> None:
        self.page.window.full_screen = e.control.value
        self._notify("Fullscreen toggled")
        self.page.update()

    def toggle_resizable(self, e: ft.ControlEvent) -> None:
        self.page.window.resizable = e.control.value
        self._notify("Resizable toggled")
        self.page.update()

    def update_window_width(self, e: ft.ControlEvent) -> None:
        try:
            width = e.control.value
            self.page.window.width = width
            self._notify(f"Window width size set to {width}")
            self.page.update()
        except ValueError:
            self.validator._show_error("Width must be numeric.")

    def update_window_height(self, e: ft.ControlEvent) -> None:
        try:
            height = e.control.value
            self.page.window.height = height
            self._notify(f"Window width size set to {height}")
            self.page.update()
        except ValueError:
            self.validator._show_error("height must be numeric.")

    def _notify(self, message: str) -> None:
        self.page.open(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.BLUE_400,
                open=True,
            )
        )
        self.page.update()
