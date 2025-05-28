# data_handler.py
import yaml


def load_project(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def save_project(path, project_data) -> None:
    with open(path, "w") as file:
        yaml.safe_dump(project_data, file, sort_keys=False)
