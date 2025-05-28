# overview.py

import flet as ft

from constants import PROJECT_CUSTOMER, PROJECT_STAGES, PROJECT_TYPES
from validation import InputValidator, ValidationType


def handle_change(e: ft.ControlEvent) -> None:
    print(f"Date changed: {e.control.value.strftime('%m/%d/%Y')}")


def handle_dismissal(e: ft.ControlEvent) -> None:
    print(ft.Text("DatePicker dismissed"))


def build_overview_tab(page: ft.Page) -> ft.Column:
    validator = InputValidator(page)

    full_name = ft.TextField(
        label="Full Name",
        width=300,
        on_blur=lambda e: validator.validate(ValidationType.NotEmpty, e),
    )
    eng_name = ft.TextField(
        label="English Name",
        width=300,
        on_change=lambda e: validator.validate(ValidationType.OnlyEnglish, e),
    )

    customer_dropdown = ft.Dropdown(
        label="Customer",
        width=300,
        options=[ft.dropdown.Option(s) for s in PROJECT_CUSTOMER],
        on_blur=lambda e: validator.validate(ValidationType.NotSelected, e),
    )

    type_dropdown = ft.Dropdown(
        label="Type",
        width=300,
        options=[ft.dropdown.Option(s) for s in PROJECT_TYPES],
        on_blur=lambda e: validator.validate(ValidationType.NotSelected, e),
    )

    # Dropdown for project stage
    stage_dropdown = ft.Dropdown(
        label="Project Stage",
        width=300,
        options=[ft.dropdown.Option(s) for s in PROJECT_STAGES],
        on_blur=lambda e: validator.validate(ValidationType.NotSelected, e),
    )
    # # Date pickers for start/end
    # date_rows: list[ft.Row] = []
    # for i in range(len(PROJECT_STAGES)):
    #     date_rows.append(
    #         ft.Row(
    #             [
    #                 ft.Text(f"Start of {PROJECT_STAGES[i]}:"),
    #                 ft.ElevatedButton(
    #                     "Pick start date",
    #                     icon=ft.Icons.CALENDAR_MONTH,
    #                     on_click=lambda e: page.open(
    #                         ft.DatePicker(
    #                             first_date=dt.datetime(
    #                                 year=2020, month=1, day=1
    #                             ),
    #                             last_date=dt.datetime(
    #                                 year=2030, month=12, day=1
    #                             ),
    #                             on_change=handle_change,
    #                             on_dismiss=handle_dismissal,
    #                         )
    #                     ),
    #                 ),
    #                 ft.Text(f"End of {PROJECT_STAGES[i]}:"),
    #                 ft.ElevatedButton(
    #                     "Pick end date",
    #                     icon=ft.Icons.CALENDAR_MONTH,
    #                     on_click=lambda e: page.open(
    #                         ft.DatePicker(
    #                             first_date=dt.datetime(
    #                                 year=2020, month=1, day=1
    #                             ),
    #                             last_date=dt.datetime(
    #                                 year=2035, month=12, day=1
    #                             ),
    #                             on_change=handle_change,
    #                             on_dismiss=handle_dismissal,
    #                         )
    #                     ),
    #                 ),
    #             ],
    #             ft.MainAxisAlignment.START,
    #         )
    #    )
    return ft.Column(
        [
            full_name,
            eng_name,
            customer_dropdown,
            type_dropdown,
            stage_dropdown,
            # *date_rows,
        ],
        spacing=10,
    )
