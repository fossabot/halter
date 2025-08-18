# src.halter.cli.project
from pathlib import Path

import typer
from rich import print

from halter.cli.context import project_ref
from halter.core.models.project import Project
from halter.core.services.config_io import load_project, save_project

app = typer.Typer(help="Create, load and save projects")


@app.command("create")
def create(name: str, description: str, area_type: list[str]) -> None:
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
    if not isinstance(p, Project):
        print("[red]No active project.[/red]")
        raise typer.Exit()
    print(p)


@app.command("save")
def save(path: Path | None = None) -> None:
    """Save project to YAML."""
    project = project_ref.get("active")
    if not isinstance(project, Project):
        print("[red]No active project.[/red]")
        raise typer.Exit()

    target = path or project_file
    save_project(project, target)
    print(f"[green]Project saved to {target}[/green]")


@app.command("load")
def load(path: Path | None = None) -> None:
    """Load project from YAML."""
    global project_file
    target = path or project_file
    try:
        project = load_project(target)
        project_ref["active"] = project
        project_file = target
        print(f"[green]Project loaded from {target}[/green]")
    except Exception as e:
        print(f"[red]Failed to load:[/red] {e}")
