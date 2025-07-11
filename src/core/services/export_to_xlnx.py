from openpyxl import Workbook


def export_to_xlsx(project, output_xlsx: str) -> None:
    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Network Configuration"

    # Write headers
    headers = ["Network Name", "IPv4 Address", "Subnet Mask", "VLAN"]
    ws.append(headers)

    # Make headers bold
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = cell.font.copy(bold=True)

    # Populate data from Project instance
    for network in project.networks:
        ws.append(
            [
                network.name,  # Direct attribute access
                network.ipv4,  # instead of .get()
                network.mask,
                network.vlan,
            ]
        )

    # Adjust column widths
    for col in range(1, len(headers) + 1):
        col_letter = chr(64 + col)
        ws.column_dimensions[col_letter].width = 18

    # Save to XLSX
    wb.save(output_xlsx)
