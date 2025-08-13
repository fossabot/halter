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

**Halter** — мультиплатформенное приложение (CLI + GUI) для планирования, моделирования и документирования сетевой инфраструктуры. Построено на модульной архитектуре с `core`, `cli` и `gui`.

---

## 🚀 Возможности

- 📦 Библиотека `halter-core` для описания сетей, оборудования и ПО
- 🔧 CLI-интерфейс `halter-cli` на основе [Typer](https://typer.tiangolo.com/)
- 🖼️ ~~GUI `halter-gui` на базе [Flet](https://flet.dev/)~~ (Пока не реализованно)
- 🧪 Тесты, линтинг, CI/CD
- 📁 Хранение конфигураций в YAML с импортом/экспортом

---

## 🛠️ Установка

### Через PyPI (будет доступно, начиная с версии 1.0)

```bash
pip install halter[cli]       # CLI только
pip install halter[gui]       # GUI только
pip install halter            # Полная установка
````

### Через TestPyPI (для тестирования и разработки)

```bash
pip install --index-url https://test.pypi.org/simple/ halter[cli]
pip install --index-url https://test.pypi.org/simple/ halter[gui]
pip install --index-url https://test.pypi.org/simple/ halter
```

---

## ⚙️ Использование

Отлично! Вот компактный **Quickstart** блок для README/DEVELOPMENT, чтобы сразу можно было попробовать Halter с CLI и GUI, плюс небольшой YAML-пример проекта.

---

### **Quickstart**

#### 1️⃣ Установка

```bash
# Для CLI
pip install halter[cli]

# Для GUI
pip install halter[gui]

# Полная установка
pip install halter
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
    vlan: 10
    address: 192.168.10.0/24
devices:
  - name: Router-1
    model: Cisco-3925
    role: core
    interfaces:
      - name: Gi0/0
        ip: 192.168.10.1
software:
  - name: DHCP
    version: "2.3"
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

---

## 👤 Автор

**HK** — [hermankriv@gmail.com](mailto:hermankriv@gmail.com)
