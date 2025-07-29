import typer
from rich import print

from core.models.project import Project

from .device import app as device_app
from .network import app as network_app
from .project import app as project_app
from .project import project_ref, save
from .software import app as software_app

app = typer.Typer(help="Project Network Architecture Planner CLI")

app.add_typer(project_app, name="project")
app.add_typer(network_app, name="network")
app.add_typer(software_app, name="software")
app.add_typer(device_app, name="device")


def run() -> None:
    try:
        app()
    finally:
        p = project_ref.get("active")
        if p is not None and isinstance(p, Project):
            try:
                save
            except Exception as e:
                print(f"[red]Auto-save failed:[/red] {e}")


# if __name__ == "__main__":
#     run()
