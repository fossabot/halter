# src/halter/cli/context.py
from pathlib import Path

from halter.core.constants import DEFAULT_PATH
from halter.core.models.project import Project

# Активный проект
project_ref: dict[str, Project] = {}

# Текущий файл проекта
project_file: Path = Path(DEFAULT_PATH)  # или импортируй DEFAULT_PATH
