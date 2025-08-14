# 🧠 Halter

[![PyPI Version](https://img.shields.io/pypi/v/halter)](https://pypi.org/project/halter/)
[![TestPyPI Version](https://img.shields.io/testpypi/v/halter)](https://test.pypi.org/project/halter/)
[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/herokrat/halter)](./docs/LICENSE.md)
[![Tests: pytest](https://img.shields.io/badge/tests-pytest-blue)](https://docs.pytest.org/)
[![Test Coverage](https://img.shields.io/badge/coverage-pytest--cov-brightgreen)](https://github.com/pytest-dev/pytest-cov)
[![Task Runner: poe](https://img.shields.io/badge/tasks-poethepoet-yellow)](https://github.com/nat-n/poethepoet)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-ff69b4.svg)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Tests Status](https://github.com/herokrat/halter/actions/workflows/tests.yml/badge.svg)](https://github.com/herokrat/halter/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/herokrat/halter/graph/badge.svg?token=SOY22473CK)](https://codecov.io/gh/herokrat/halter)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Docs: mkdocs](https://img.shields.io/badge/docs-mkdocs-blue)](https://herokrat.github.io/halter/)
[![Made with Typer](https://img.shields.io/badge/-Made%20with%20Typer-important?logo=python&logoColor=white)](https://typer.tiangolo.com/)
[![Flet GUI](https://img.shields.io/badge/Flet-GUI_Support-9cf)](https://flet.dev)

![Logo](/src/halter/assets/logo.jpg "Halter")

**Halter** — мультиплатформенное приложение (CLI + GUI) для планирования, моделирования и документирования сетевой инфраструктуры. Построено на модульной архитектуре с `core`, `cli` и `gui`.

---

## 🚀 Возможности

- 📦 Библиотека `halter-core` для описания сетей, оборудования и ПО
- 🔧 CLI-интерфейс `halter-cli` на основе [Typer](https://typer.tiangolo.com/)
- 🖼️ ~~GUI `halter-gui` на базе [Flet](https://flet.dev/)~~ (Пока не реализованно)
- 🧪 Тесты, линтинг, CI/CD
- 📁 Хранение конфигураций в YAML с импортом/экспортом

---

## ⚙️ Использование

### **Quickstart**

#### 1️⃣ Установка

Через PyPI (будет доступно, начиная с версии 1.0)

```bash
pip install halter[cli]       # CLI только
pip install halter[gui]       # GUI только
pip install halter            # Полная установка
```

Через TestPyPI (для тестирования и разработки)

```bash
pip install --index-url https://test.pypi.org/simple/ halter[cli]
pip install --index-url https://test.pypi.org/simple/ halter[gui]
pip install --index-url https://test.pypi.org/simple/ halter
```

---

#### 2️⃣ Пример использования CLI

```bash
# Создаем устройство
halter-cli add device --name "Router-1" --model "Cisco-3925" --role "core"

# Список устройств
halter-cli list devices

# Добавление сети
halter-cli add network --name "LAN-1" --vlan 10 --address 192.168.10.0/24

# Привязка устройства к сети
halter-cli attach device --device "Router-1" --network "LAN-1"
```

---

#### 3️⃣ Пример использования GUI

```bash
python -m halter.gui.main
```

> GUI позволяет визуально создавать устройства, сети, ПО и просматривать связи между ними.

---

#### 4️⃣ Пример YAML проекта

Создадим файл `project.yaml`:

```yaml
name: OfficeNetwork
description: Сеть офисного здания
area_type:
  - office
networks:
  - name: LAN-1
    description: Сеть офиса
    vlan:
      id: 10
      name: IT
    topology: Star
    address_type: IPv4 Network
    address: 192.168.10.0/24
devices:
  - name: Router-1
    model: Cisco-3925
    role: router
    interfaces:
      - name: Gi0/0
        network_id: LAN-1
        routes: []
        address_type: IPv4 Address
        address: 192.168.10.1
        vlan_mode: Access
        software_id: cisco_networking
software:
  - name: DHCP
    version: "2.3"
  - name:  cisco_networking
    version: "1.0"
```

---

#### 5️⃣ Загрузка YAML в Halter

```bash
halter-cli import project.yaml
halter-cli list devices
halter-cli list networks
```

> Теперь можно работать с проектом как через CLI, так и через GUI.

---

## 🗂️ Структура проекта

```text
halter/
|────src/
|    |──halter/
|        ├── core/        # Логика приложения
|        ├── cli/         # Консольное приложение
|        ├── gui/         # Графический интерфейс
├── tests/       # Тесты
├── docs/        # Документация
├── pyproject.toml
├── README.md
```

---

## 📝 Лицензия

[MIT License](docs/LICENSE.md)

## Разработка

Руководство по разработке представлено в отдельном файле [DEVELOPMENT](docs/DEVELOPMENT.md)

---

## 👤 Автор

**HK** — [hermankriv@gmail.com](mailto:hermankriv@gmail.com)
