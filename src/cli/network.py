import typer
from rich import print

from cli.project import project_ref
from core.models.network import Network

app = typer.Typer(help="Manage networks in the active project")


@app.command("add")
def add(
    name: str = typer.Option(..., help="NetBIOS name (≤15 chars)"),
    ipv4: str = typer.Option(..., help="IPv4 address"),
    mask: str = typer.Option(..., help="Subnet mask"),
    vlan: int = typer.Option(..., help="VLAN ID (1–4094)"),
) -> None:
    """Add a new network to the active project."""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project. Use `project create` first.[/red]")
        raise typer.Exit()

    try:
        net = Network(name=name, ipv4=ipv4, mask=mask, vlan=vlan)
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
        print(
            f"[cyan]{idx}. {net.name}[/cyan]| IP: {net.ipv4}| Mask: {net.mask}\
                | VLAN: {net.vlan}"
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
    name: str = typer.Argument(..., help="Existing network name to edit"),
    ipv4: str = typer.Option(None, help="New IPv4"),
    mask: str = typer.Option(None, help="New mask"),
    vlan: int = typer.Option(None, help="New VLAN"),
):
    """Edit a network’s properties."""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project.[/red]")
        raise typer.Exit()

    for net in project.networks:
        if net.name == name:
            if ipv4:
                net.ipv4 = ipv4
            if mask:
                net.mask = mask
            if vlan:
                net.vlan = vlan
            try:
                net.__post_init__()  # Re-validate
                print(f"[green]Network '{name}' updated.[/green]")
            except ValueError as e:
                print(f"[red]Validation failed:[/red] {e}")
            return

    print(f"[yellow]Network '{name}' not found.[/yellow]")
