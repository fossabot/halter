# src/core/services/export_to_xlnx.py
import ipaddress

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet

from halter.core.models.project import Project


def export_to_xlsx(project: Project, output_xlsx: str) -> None:
    # Create Excel workbook
    wb = Workbook()
    ws: Worksheet = wb.active  # type: ignore
    ws.title = "Network Configuration"

    # Write headers
    headers = [
        "#",
        "Network Name",
        "Address Type",
        "Address",
        "Subnet Mask",
        "VLAN",
        "Topology",
    ]
    ws.append(headers)

    # Make headers bold
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = Font(bold=True)

    i: int = 0
    # Populate data from Project instance
    for network in project.networks:
        i = i + 1
        ws.append(
            [
                i,
                network.name,  # Direct attribute access
                network.address_type,
                str(
                    ipaddress.ip_network(
                        network.address, strict=False
                    ).network_address
                )
                if network.address_type == "IPv4 Network"
                else "",
                str(
                    ipaddress.ip_network(network.address, strict=False).netmask
                )
                if network.address_type == "IPv4 Network"
                else "",
                network.vlan.id if network.vlan is not None else "",
                network.topology,
            ]
        )

    # Adjust column widths
    for col in range(1, len(headers) + 1):
        col_letter = chr(64 + col)
        ws.column_dimensions[col_letter].width = 18

    for area_type in project.area_type:
        worksheet: Worksheet = wb.create_sheet(area_type.upper())
        worksheet.append(area_type.upper())

    # Save to XLSX
    wb.save(output_xlsx)
