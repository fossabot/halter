import typer
from rich import print

from halter.cli.context import project_ref
from halter.core.models.device import Device
from halter.core.models.interface import NetworkInterface

app = typer.Typer(help="Manage devices in the active project")


@app.command("add")
def add(
    name: str = typer.Option(..., help="NetBIOS name (≤15 chars)"),
    description: str = typer.Option(..., help="Device description"),
    model: str = typer.Option(..., help="Device model"),
    role: str = typer.Option(
        ..., help="router | switch | ntp server | workstation | panel"
    ),
    interfaces: int = typer.Option(1, help="Number of network interfaces"),
) -> None:
    """Add a device with specified number of interfaces"""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project found.[/red]")
        raise typer.Exit()

    if len(name) > 15:
        print("[red]NetBIOS name must be 15 characters or fewer.[/red]")
        raise typer.Exit()

    net_names = [n.name for n in project.networks]
    if not net_names:
        print(
            "[yellow]Warning: No networks defined. Interfaces may fail validation.[/yellow]"
        )

    interfaces_list = []
    for i in range(interfaces):
        print(f"[blue]Configuring interface #{i + 1}[/blue]")

        iface_name = typer.prompt("Interface name")
        net_id = typer.prompt(f"Network name (one of: {net_names})")
        address = typer.prompt("IPv4 address")
        routes_str = typer.prompt("Routes (comma separated IPv4s)", default="")
        address_type = typer.prompt("Address type", default="IPv4 Address")
        vlan_mode = typer.prompt("Vlan mode", default="Access")
        software_id = typer.prompt("Software id")
        route_list = [r.strip() for r in routes_str.split(",") if r.strip()]
        try:
            iface = NetworkInterface(
                name=iface_name,
                network_id=net_id,
                address=address,
                routes=route_list,
                address_type=address_type,
                vlan_mode=vlan_mode,
                software_id=software_id,
            )
            interfaces_list.append(iface)
        except ValueError as e:
            print(f"[red]Interface error:[/red] {e}")
            raise typer.Exit()

    device = Device(
        name=name,
        description=description,
        model=model,
        role=role,
        interfaces=interfaces_list,
    )
    project.devices.append(device)
    print(f"[green]Device '{name}' added.[/green]")


@app.command("list")
def list_devices() -> None:
    """List all devices"""
    project = project_ref.get("active")
    if not project or not project.devices:
        print("[yellow]No devices to show.[/yellow]")
        return

    for d in project.devices:
        print(
            f"[cyan]{d.name}[/cyan] | {d.role} | Interfaces: {len(d.interfaces)}"
        )


@app.command("delete")
def delete(name: str) -> None:
    """Delete a device by name"""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project.[/red]")
        raise typer.Exit()

    before = len(project.devices)
    project.devices = [d for d in project.devices if d.name != name]
    if len(project.devices) == before:
        print(f"[yellow]No device named '{name}' found.[/yellow]")
    else:
        print(f"[green]Device '{name}' deleted.[/green]")


@app.command("list-interfaces")
def list_interfaces(name: str) -> None:
    """List of interfaces of current device"""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project.[/red]")
        raise typer.Exit()
    for d in project.devices:
        if d.name == name:
            device = d
    else:
        if device is None:
            print(f"[yellow]No device named '{name}' found.[/yellow]")
    for interface in device.interfaces:
        print(f"[cyan]{interface.name}[/cyan]")
