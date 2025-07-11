import flet as ft

from .color_picker import ColorPicker
from .validation import InputValidator, ValidationType


def build_network(page: ft.Page) -> ft.Card:
    card_container = ft.Container(
        width=300,
        expand=True,
        padding=10,
        adaptive=True,
    )

    def on_color_change(color: dict) -> None:
        card_container.bgcolor = color["bg"]
        text_color = color["text"]

        # Обновляем цвет текста всех вложенных полей
        for ctrl in [net_name, net_class, ip_addr, mask, vlan, gateway]:
            ctrl.color = text_color
            if hasattr(ctrl, "border_color"):
                ctrl.border_color = (
                    text_color  # если хочешь и бордер перекрасить
                )

        page.update()

    validator = InputValidator(page)
    net_name = ft.TextField(
        value="LocalNetwork",
        label="Network Name",
        adaptive=True,
        width=300,
        on_blur=lambda e: validator.validate(ValidationType.NotEmpty, e),
    )
    net_class = ft.Dropdown(
        value="A",
        label="Class",
        options=[ft.dropdown.Option(c) for c in ["A", "B", "C"]],
        width=300,
        on_blur=lambda e: validator.validate(ValidationType.NotSelected, e),
    )
    mask = ft.Dropdown(
        value="8",
        label="Mask",
        options=[ft.dropdown.Option(str(i)) for i in range(8, 31)],
        on_blur=lambda e: validator.validate(ValidationType.NotSelected, e),
    )
    ip_addr = ft.TextField(
        value="127.0.0.0",
        label="IPv4 Address",
        width=300,
        adaptive=True,
        on_blur=lambda e: validator.validate(
            ValidationType.IPv4NetworkAddress, e, mask.value
        ),
    )

    vlan = ft.TextField(
        value="1",
        label="VLAN ID",
        on_blur=lambda e: validator.validate(ValidationType.VLAN, e),
        width=300,
        adaptive=True,
    )
    gateway = ft.TextField(
        value="127.0.0.1",
        label="IPv4 Address",
        width=300,
        adaptive=True,
        on_blur=lambda e: validator.validate(
            ValidationType.IPv4HostAddress, e, mask.value, ip_addr.value
        ),
    )
    color = ColorPicker(on_color_change=on_color_change)

    card_container.content = ft.Column(
        [net_name, net_class, ip_addr, mask, vlan, gateway, color]
    )

    return ft.Card(content=card_container)


def build_network_container(page: ft.Page) -> ft.Container:
    cards: list[ft.Card] = [
        build_network(page) for _ in range(4)
    ]  # Пример: 10 карточек

    grid = ft.GridView(expand=True, spacing=10, run_spacing=10, adaptive=True)

    def update_grid_layout(e=None) -> None:
        width = page.window.width or 800  # fallback если не определилось
        card_width = 320  # ширина одной карточки + отступы
        cols = max(1, width // card_width)

        # Расчёт max_extent, который даёт гриду понять, сколько карточек помещать
        grid.max_extent = width / cols - 20

        page.update()

    # Начальная инициализация
    grid.controls = cards
    update_grid_layout()

    # Обработка изменения размера окна
    page.window.on_event = update_grid_layout

    return ft.Container(expand=True, content=grid, adaptive=True)
