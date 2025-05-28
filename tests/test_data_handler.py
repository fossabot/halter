import os
import tempfile

import yaml

from src import data_handler  # замените your_module на имя файла с функциями


def test_load_project_reads_yaml_correctly() -> None:
    data = {"name": "Test Project", "value": 123}
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        yaml.safe_dump(data, tmp)
        tmp_path = tmp.name

    loaded = data_handler.load_project(tmp_path)
    os.unlink(tmp_path)  # удаляем временный файл после теста

    assert loaded == data


def test_save_project_writes_yaml_correctly() -> None:
    data = {"name": "Saved Project", "items": [1, 2, 3]}
    with tempfile.NamedTemporaryFile("r+", delete=False) as tmp:
        tmp_path = tmp.name

    data_handler.save_project(tmp_path, data)

    with open(tmp_path, "r") as f:
        loaded = yaml.safe_load(f)
    os.unlink(tmp_path)

    assert loaded == data
