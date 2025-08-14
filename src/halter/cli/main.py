from pathlib import Path

import typer
from rich import print

from halter.core.constants import DEFAULT_EXPORT_PATH
from halter.core.models.project import Project
from halter.core.services.export.firewall import export_firewall_configs
from halter.core.services.export.netmap import export_to_xlsx
from halter.core.services.export.network_config import (
    export_networking_configs,
)

from .device import app as device_app
from .network import app as network_app
from .project import app as project_app
from .project import project_ref, save
from .software import app as software_app

app = typer.Typer(help="Project Network Architecture Planner CLI")

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
                save
            except Exception as e:
                print(f"[red]Auto-save failed:[/red] {e}")


# if __name__ == "__main__":
#     run()


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
