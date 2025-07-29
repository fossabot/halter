# 🧠 Halter

![Logo](/src/assets/logo.jpg "Halter")
![Tests](https://github.com/herokrat/halter/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/herokrat/halter/graph/badge.svg?token=SOY22473CK)](https://codecov.io/gh/herokrat/halter)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)
![License](https://img.shields.io/github/license/herokrat/halter)
[![Made with Typer](https://img.shields.io/badge/-Made%20with%20Typer-green?logo=python&logoColor=white)](https://github.com/tiangolo/typer)
[![Made with Flet](https://img.shields.io/badge/Made%20with-Flet-blue?logo=flutter)](https://flet.dev/)
![Build](https://img.shields.io/github/actions/workflow/status/herokrat/halter/tests.yml?label=build)
[![Last commit](https://img.shields.io/github/last-commit/herokrat/halter)](https://github.com/herokrat/halter/commits/main)
[![Issues](https://img.shields.io/github/issues/herokrat/halter)](https://github.com/herokrat/halter/issues)
[![PRs](https://img.shields.io/github/issues-pr/herokrat/halter)](https://github.com/herokrat/halter/pulls)

**Halter** — это мультиплатформенное приложение (CLI + GUI) для планирования, моделирования и документирования сетевой инфраструктуры. Построено на модульной архитектуре с разделением на `core`, `cli` и `gui`.

---

## 🚀 Возможности

- 📦 Мощная библиотека `halter-core` для описания сетей, оборудования и ПО
- 🔧 Удобный CLI-интерфейс `halter-cli` на основе [Typer](https://typer.tiangolo.com/)
- 🖼️ Современный GUI `halter-gui` на базе [Flet](https://flet.dev/)
- 🧪 Покрытие тестами, линтинг, CI/CD.
- 📁 Хранение конфигураций в YAML с возможностью импорта/экспорта
- 🛠️ Структура монорепозитория с `hatch` и `uv`

---

## 🛠️ Установка

### 1. Установите [uv](https://github.com/astral-sh/uv) и [hatch](https://hatch.pypa.io/)

```bash
pip install uv hatch
````

### 2. Клонируйте репозиторий и установите зависимости

```bash
git clone https://github.com/herokrat/halter.git
cd halter
uv venv
uv pip install .
```

---

## ⚙️ Использование

### CLI

```bash
halter-cli --help
```

Пример:

```bash
halter-cli add device --name "Router-1" --ip 10.0.0.1
```

### GUI

```bash
uv run halter-gui
```

---

## 🧪 Тестирование

```bash
hatch run test
```

---

## 🧼 Линтинг и форматирование

```bash
hatch run lint
hatch run format
```

---

## 📦 Сборка

```bash
make build
```

---

## 📤 Публикация на PyPI

Убедитесь, что у вас установлен `PYPI_TOKEN` в GitHub Secrets или `.env`:

```bash
make publish
```

---

## 🗂️ Структура проекта

```bash
halter/
├── core/        # Библиотека с логикой
├── cli/         # Консольное приложение
├── gui/         # Графический интерфейс
├── tests/       # Тесты
├── pyproject.toml
├── Makefile
```

---

## 🧠 Зависимости

- Python ≥ 3.13
- [Typer](https://typer.tiangolo.com/)
- [Flet](https://flet.dev/)
- [uv](https://github.com/astral-sh/uv)
- [hatch](https://hatch.pypa.io/)
- [pytest](https://docs.pytest.org/)
- [ruff](https://docs.astral.sh/ruff/)

---

## 📝 Лицензия

[MIT License](./LICENSE)

---

## 👤 Автор

**HK** — [hk@example.com](mailto:hk@example.com)

---
