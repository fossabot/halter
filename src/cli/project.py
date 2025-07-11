from pathlib import Path

import typer
from rich import print

from core.constants import DEFAULT_PATH
from core.models.project import Project
from core.services.config_io import load_project, save_project
from core.services.export_to_xlnx import export_to_xlsx

app = typer.Typer(help="Create, load and save projects")

# In-memory reference
project_ref: dict[str, Project] = {}


# Auto-load on module import
if Path(DEFAULT_PATH).exists():
    try:
        project = load_project(DEFAULT_PATH)
        if isinstance(project, Project):
            project_ref["active"] = project
            print(f"[blue]Auto-loaded project from {DEFAULT_PATH}[/blue]")
        else:
            print(
                f"[yellow]Warning: {DEFAULT_PATH} does not contain a valid project.[/yellow]"
            )
    except Exception as e:
        print(f"[red]Failed to auto-load project.yaml:[/red] {e}")


@app.command("create")
def create(name: str, description: str, area_type: str) -> None:
    """Create a new project"""
    try:
        p = Project(name=name, description=description, area_type=area_type)
        project_ref["active"] = p
        print(f"[green]Project '{name}' created.[/green]")
        save()
    except ValueError as e:
        print(f"[red]Error:[/red] {e}")


@app.command("summary")
def summary() -> None:
    """Show project summary"""
    p = project_ref.get("active")
    if not p:
        print("[red]No active project.[/red]")
        raise typer.Exit()
    print(p)


@app.command("save")
def save(path: str = DEFAULT_PATH) -> None:
    """Save project to YAML."""
    project = project_ref.get("active")
    if not project:
        print("[red]No active project.[/red]")
        raise typer.Exit()
    save_project(project, path)
    print(f"[green]Project saved to {path}[/green]")


@app.command("load")
def load(
    path: str = DEFAULT_PATH,
) -> None:
    """Load project from YAML."""
    try:
        project = load_project(path)
        project_ref["active"] = project
        print(f"[green]Project loaded from {path}[/green]")
    except Exception as e:
        print(f"[red]Failed to load:[/red] {e}")


@app.command("export-netmap")
def export_netmap(path: str = "network_ips.xlsx") -> None:
    """Show project summary"""
    p = project_ref.get("active")
    if not p:
        print("[red]No active project.[/red]")
        raise typer.Exit()
    export_to_xlsx(p, path)
