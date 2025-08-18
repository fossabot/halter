# src.halter.cli.main
from pathlib import Path

import typer
from rich import print

from halter.core.constants import DEFAULT_EXPORT_PATH, DEFAULT_PATH
from halter.core.models.project import Project
from halter.core.services.config_io import load_project, save_project
from halter.core.services.export.firewall import export_firewall_configs
from halter.core.services.export.netmap import export_to_xlsx
from halter.core.services.export.network_config import (
    export_networking_configs,
)

from .context import project_file, project_ref
from .device import app as device_app
from .network import app as network_app
from .project import app as project_app
from .software import app as software_app

app = typer.Typer(help="Project Network Architecture Planner CLI")


@app.callback()
def global_init(
    file: Path = typer.Option(
        Path(DEFAULT_PATH),
        "-f",
        "--file",
        help="Path to the project YAML file",
    ),
) -> None:
    """
    Глобальный callback: загружает проект при любом запуске CLI.
    """
    global project_file
    project_file = file

    if project_file.exists():
        try:
            project = load_project(project_file)
            if isinstance(project, Project):
                project_ref["active"] = project
                print(f"[blue]Auto-loaded project from {project_file}[/blue]")
            else:
                print(
                    f"[yellow]Warning: Invalid project data in {project_file}[/yellow]"
                )
        except Exception as e:
            print(f"[red]Failed to load {project_file}:[/red] {e}")
    else:
        # Создаём дефолтный проект, если файл не существует
        project = Project(
            name="Default name",
            description="Description",
            area_type=["Other"],
            networks=[],
            devices=[],
            software=[],
        )
        project_ref["active"] = project
        print(f"[blue]Default project created `{project.name}`[/blue]")


app.add_typer(project_app, name="project")
app.add_typer(software_app, name="software")
app.add_typer(network_app, name="network")
app.add_typer(device_app, name="device")


def run() -> None:
    try:
        app()
    finally:
        p = project_ref.get("active")
        if p is not None and isinstance(p, Project):
            try:
                save_project(p, project_file)
            except Exception as e:
                print(f"[red]Auto-save failed:[/red] {e}")


@app.command("export-netmap")
def export_netmap(path: str = "network_ips.xlsx") -> None:
    """Export netmap in xlsx format"""
    p = project_ref.get("active")
    if not p:
        print("[red]No active project.[/red]")
        raise typer.Exit()
    export_to_xlsx(p, path)


@app.command("export-configs")
def export_configs(path: Path = Path(DEFAULT_EXPORT_PATH)) -> None:
    """Export all device configs"""
    p = project_ref.get("active")
    if not p:
        print("[red]No active project.[/red]")
        raise typer.Exit()
    export_networking_configs(project=p, output_dir=path)
    export_firewall_configs(project=p, output_dir=path)
