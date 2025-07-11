import typer
from rich import print

from cli.project import project_ref
from core.models.software import Software

app = typer.Typer(help="Manage software entries in the active project")


@app.command("add")
def add(
    name: str,
    description: str,
    version: str,
    has_net: bool = typer.Option(False, help="Has network capabilities?"),
    input_port: int = typer.Option(None, help="Input port (if networked)"),
    output_port: int = typer.Option(None, help="Output port (if networked)"),
):
    """Add a software entry."""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project found.[/red]")
        raise typer.Exit()

    try:
        sw = Software(
            name=name,
            description=description,
            version=version,
            has_network_capability=has_net,
            input_port=input_port,
            output_port=output_port,
        )
        project.software.append(sw)
        print(f"[green]Software '{name}' added.[/green]")
    except ValueError as e:
        print(f"[red]Error:[/red] {e}")


@app.command("list")
def list_software():
    """List all software in the project"""
    project = project_ref.get("active")
    if not project or not project.software:
        print("[yellow]No software entries found.[/yellow]")
        return

    for s in project.software:
        net = "🌐" if s.has_network_capability else "—"
        print(f"[cyan]{s.name}[/cyan] | {s.version} | Net: {net}")


@app.command("delete")
def delete(name: str):
    """Delete software by name"""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project.[/red]")
        raise typer.Exit()

    before = len(project.software)
    project.software = [s for s in project.software if s.name != name]
    if len(project.software) == before:
        print(f"[yellow]No software named '{name}' found.[/yellow]")
    else:
        print(f"[green]Software '{name}' deleted.[/green]")
