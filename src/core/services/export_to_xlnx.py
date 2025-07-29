# src/core/services/export_to_xlnx.py
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet

from core.models.project import Project


def export_to_xlsx(project: Project, output_xlsx: str) -> None:
    # Create Excel workbook
    wb = Workbook()
    ws: Worksheet = wb.active  # type: ignore
    ws.title = "Network Configuration"

    # Write headers
    headers = ["Network Name", "IPv4 Address", "Subnet Mask", "VLAN"]
    ws.append(headers)

    # Make headers bold
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = Font(bold=True)

    # Populate data from Project instance
    for network in project.networks:
        ws.append(
            [
                network.name,  # Direct attribute access
                network.address,  # instead of .get()
                # network.vlan.id,
            ]
        )

    # Adjust column widths
    for col in range(1, len(headers) + 1):
        col_letter = chr(64 + col)
        ws.column_dimensions[col_letter].width = 18

    # Save to XLSX
    wb.save(output_xlsx)
