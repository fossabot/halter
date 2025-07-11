import typer
from rich import print

from cli import device, network, project, software
from core.constants import DEFAULT_PATH

app = typer.Typer(help="Project Network Architecture Planner CLI")

app.add_typer(project.app, name="project")
app.add_typer(network.app, name="network")
app.add_typer(device.app, name="device")
app.add_typer(software.app, name="software")


def run() -> None:
    try:
        app()
    finally:
        project_data = project.project_ref.get("active")
        if project is not None:  # and isinstance(project, project.Project):
            try:
                project.save_project(project_data, DEFAULT_PATH)
                print(f"[green]Project auto-saved to {DEFAULT_PATH}[/green]")
            except Exception as e:
                print(f"[red]Auto-save failed:[/red] {e}")


# if __name__ == "__main__":
#     run()
