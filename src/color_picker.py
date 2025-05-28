import flet as ft

from constants import COLORS


class ColorPicker(ft.ElevatedButton):
    def __init__(
        self,
        initial_color: str = "#FFFFFF",
        on_color_change=None,
    ) -> None:
        super().__init__()

        self.selected_color: str = initial_color
        self.on_color_change = on_color_change

        # Настройка внешнего вида
        self.text = self.selected_color
        # self.bgcolor = self.selected_color
        self.on_click = self._on_click

    def _on_click(self, e: ft.ControlEvent) -> None:
        self.page: ft.Page = e.page
        self.grid = ft.GridView(
            expand=1,
            runs_count=4,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )
        # Кнопки цветов
        for color in COLORS:
            self.grid.controls.append(
                ft.Container(
                    width=30,
                    height=30,
                    bgcolor=color["bg"],
                    border_radius=5,
                    on_click=self._get_color_select_handler(color),
                )
            )

        # Диалог
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Select a color"),
            content=self.grid,
            actions=[ft.TextButton("Close", on_click=lambda e: self.page.close(self.dialog))],
        )

        # Открытие диалога через page.open
        self.page.open(self.dialog)

    # В _get_color_select_handler:
    def _get_color_select_handler(self, color: dict):
        def handler(e: ft.ControlEvent) -> None:
            self.selected_color = color["bg"]
            self.text = color["bg"]
            self.bgcolor = color["bg"]
            self.update()
            self.page.close(self.dialog)

            if self.on_color_change:
                self.on_color_change(color)

        return handler
