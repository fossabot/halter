import typer
from rich import print

from halter.cli.context import project_ref
from halter.core.models.address import AddressingType
from halter.core.models.network import (
    VLAN,
    Network,
    NetworkTier,
    NetworkTopology,
)

app = typer.Typer(help="Manage networks in the active project")


@app.command("add")
def add(
    name: str = typer.Option(..., help="Network name"),
    description: str = typer.Option(..., help="Network description"),
    topology: NetworkTopology = typer.Option(..., help="Network topology"),
    tier: NetworkTier = typer.Option(..., help="Network tier"),
    address_type: AddressingType = typer.Option(..., help="Addressing type"),
    address: str = typer.Option(
        ..., help="Network address (e.g., 192.168.1.0/24)"
    ),
    vlan_id: int = typer.Option(..., help="VLAN ID (1-4094)"),
    vlan_name: str = typer.Option(..., help="VLAN name"),
    gateway: str = typer.Option(..., help="Gateway"),
) -> None:
    """Add a new network to the active project."""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project. Use `project create` first.[/red]")
        raise typer.Exit()

    try:
        vlan = VLAN(id=vlan_id, name=vlan_name)
        net = Network(
            name=name,
            description=description,
            vlan=vlan,
            topology=topology,
            tier=tier,
            address_type=address_type,
            address=address,
            gateway=gateway,
        )
        project.networks.append(net)
        print(f"[green]Added network '{name}'[/green]")
    except ValueError as e:
        print(f"[red]Invalid input:[/red] {e}")


@app.command("list")
def list_networks() -> None:
    """List all networks in the active project."""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project.[/red]")
        raise typer.Exit()

    if not project.networks:
        print("[yellow]No networks found.[/yellow]")
        return

    for idx, net in enumerate(project.networks, 1):
        vlan_str = f"{net.vlan.id} ({net.vlan.name})" if net.vlan else "None"
        print(
            f"[cyan]{idx}. {net.name}[/cyan] | IP: {net.address} | VLAN: {vlan_str} | Topology: {net.topology.value} | Tier: {net.tier.value} | Gateway: {net.gateway}"
        )


@app.command("delete")
def delete(name: str) -> None:
    """Delete a network by name."""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project.[/red]")
        raise typer.Exit()

    before = len(project.networks)
    project.networks = [n for n in project.networks if n.name != name]
    after = len(project.networks)

    if before == after:
        print(f"[yellow]No network named '{name}' found.[/yellow]")
    else:
        print(f"[green]Deleted network '{name}'[/green]")


@app.command("edit")
def edit(
    name: str = typer.Argument(..., help="Network name to edit"),
    description: str = typer.Option(None, help="New description"),
    address: str = typer.Option(None, help="New address"),
    address_type: AddressingType = typer.Option(None, help="New address type"),
    vlan_id: int = typer.Option(None, help="New VLAN ID"),
    vlan_name: str = typer.Option(None, help="New VLAN name"),
    topology: NetworkTopology = typer.Option(
        None, help="New network topology"
    ),
    tier: NetworkTier = typer.Option(None, help="New network tier"),
    gateway: str = typer.Option(None, help="Gateway"),
) -> None:
    """Edit an existing network."""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project.[/red]")
        raise typer.Exit()

    for net in project.networks:
        if net.name == name:
            try:
                if address:
                    net.update_address(
                        address, address_type or net.address_type
                    )
                if description:
                    net.description = description
                if vlan_id and vlan_name:
                    net.vlan = VLAN(id=vlan_id, name=vlan_name)
                if topology:
                    net.topology = topology
                if tier:
                    net.tier = tier
                if gateway:
                    net.gateway = gateway
                print(f"[green]Updated network '{name}'.[/green]")
            except ValueError as e:
                print(f"[red]Validation failed:[/red] {e}")
            return

    print(f"[yellow]Network '{name}' not found.[/yellow]")


@app.command("show")
def show(name: str = typer.Argument(..., help="Network name to show")) -> None:
    """Show detailed info about a network."""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project.[/red]")
        raise typer.Exit()

    for net in project.networks:
        if net.name == name:
            vlan = f"{net.vlan.id} ({net.vlan.name})" if net.vlan else "None"
            print(f"[cyan]Network: {net.name}[/cyan]")
            print(f"  Description   : {net.description}")
            print(f"  Address       : {net.address}")
            print(f"  Address Type  : {net.address_type.value}")
            print(f"  VLAN          : {vlan}")
            print(f"  Topology      : {net.topology.value}")
            print(f"  Tier          : {net.tier.value}")
            print(f"  Gateway       : {net.gateway}")
            return

    print(f"[yellow]Network '{name}' not found.[/yellow]")
