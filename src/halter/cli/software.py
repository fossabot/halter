import typer
from rich import print
from rich.table import Table

from halter.cli.context import project_ref
from halter.core.models.software import Direction, Port, Protocol, Software

app = typer.Typer(help="Manage software entries in the active project")


@app.command("add")
def add(
    name: str,
    description: str,
    version: str,
) -> None:
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
        )
        project.software.append(sw)
        print(f"[green]Software '{name}' added.[/green]")
    except ValueError as e:
        print(f"[red]Error:[/red] {e}")


@app.command("list")
def list_software() -> None:
    """List all software in the project"""
    project = project_ref.get("active")
    if not project or not project.software:
        print("[yellow]No software entries found.[/yellow]")
        return

    for s in project.software:
        print(f"[cyan]{s.name}[/cyan] | {s.version}")


@app.command("list-ports")
def list_ports(
    software_name: str = typer.Argument(..., help="Название ПО"),
) -> None:
    """Вывести список портов у выбранного ПО"""
    project = project_ref.get("active")
    if not project or not project.software:
        print("[yellow] Нет записей ПО в проекте.[/yellow]")
        return

    # Поиск ПО по имени
    software = next(
        (sw for sw in project.software if sw.name == software_name), None
    )

    if software is None:
        print(f"[red] ПО с названием '{software_name}' не найдено.[/red]")
        return

    if not software.ports:
        print(f"[blue]ℹ У ПО '{software.name}' нет портов.[/blue]")
        return

    table = Table(title=f"Порты для {software.name}")
    table.add_column("№", style="dim", width=4)
    table.add_column("Направление", justify="center")
    table.add_column("Протокол", justify="center")
    table.add_column("Номер порта", justify="center")
    table.add_column("Описание")

    for i, port in enumerate(software.ports):
        table.add_row(
            str(i),
            port.direction,
            port.protocol,
            str(port.index),
            port.description,
        )

    print(table)


@app.command("delete")
def delete(name: str) -> None:
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


@app.command("add-port")
def add_port(
    software_name: str = typer.Argument(..., help="Название ПО в списке"),
    direction: Direction = typer.Option(..., help="inbound или outbound"),
    protocol: Protocol = typer.Option(..., help="TCP или UDP"),
    port_index: int = typer.Option(..., help="Номер порта"),
    description: str = typer.Option("", help="Описание"),
) -> None:
    project = project_ref.get("active")
    if not project:
        print("[red]No active project found.[/red]")
        raise typer.Exit()

    try:
        software = next(s for s in project.software if s.name == software_name)
        new_port = Port(
            direction=direction,
            protocol=protocol,
            index=port_index,
            description=description,
        )
        software.ports.append(new_port)
        typer.echo(
            f"[green] Порт {protocol}:{port_index} добавлен в {software.name} [/green]"
        )
    except ValueError as e:
        print(f"[red]Error:[/red] {e}")


@app.command("remove-port")
def remove_port(
    software_name: str = typer.Argument(..., help="Название ПО в списке"),
    port_index: int = typer.Argument(
        ..., help="Индекс порта в software.ports"
    ),
) -> None:
    project = project_ref.get("active")
    if not project:
        print("[red]No active project found.[/red]")
        raise typer.Exit()

    try:
        software = next(s for s in project.software if s.name == software_name)
        removed = software.ports.pop(port_index)
        print(
            f"[yellow] Удалён порт {removed.protocol}:{removed.index} из {software.name}[/yellow]"
        )
    except IndexError:
        print(f"[red]Неверный индекс порта {port_index}[/red]")


@app.command("edit-port")
def edit_port(
    software_name: str = typer.Argument(..., help="Название ПО в списке"),
    port_index: int = typer.Argument(
        ..., help="Индекс порта в software.ports"
    ),
    direction: Direction = typer.Option(None),
    protocol: Protocol = typer.Option(None),
    port: int = typer.Option(None),
    description: str = typer.Option(None),
) -> None:
    project = project_ref.get("active")
    if not project:
        print("[red]No active project found.[/red]")
        raise typer.Exit()

    try:
        software = next(s for s in project.software if s.name == software_name)
        p = software.ports[port_index]
        if direction:
            p.direction = direction
        if protocol:
            p.protocol = protocol
        if port is not None:
            p.index = port
        if description:
            p.description = description
        print(
            f"[yellow]Порт #{port_index} отредактирован в {software.name} [/yellow]"
        )
    except IndexError:
        print("[red] Неверный индекс порта [/red]")
