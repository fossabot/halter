# 🛠️ Разработка Halter

## 🔧 Разработка и установка

### Подготовка среды разработки

Лучшие всего использовать пакетный менеджер: uv, но возможна и работа через обычный pip.

Установка uv (<https://docs.astral.sh/uv/getting-started/installation/>)

Копирование и настройка репозитория через uv и создание виртуального окружения .

```bash
git clone https://github.com/herokrat/halter.git
cd halter
uv venv
.\.venv\Scripts\activate.bat  # Windows
source .venv/bin/activate # Linux
uv sync          # Устанавливает обычные зависимости
uv add --dev     # Устанавливает все dev-зависимости
```

Копирование и настройка репозитория через встроенный pip и создание виртуального окружения.

```bash
git clone https://github.com/herokrat/halter.git
cd halter
python -m venv .venv
.\.venv\Scripts\activate.bat  # Windows
source .venv/bin/activate # Linux
pip install requirements.txt
```

---

## 🧪 Тестирование

```bash
pytest
pytest --cov
mypy src
ruff check src
mkdocs build
mkdocs server
```

Либо использовать [Poe](https://poethepoet.natn.io), где созданы псевдонимы команд.

```bash
poe test
poe check
poe format
poe docs
poe docs-test
```

---

## 📦 Сборка приложения

Сбока производится с помощью build-backend `uv-build`, собранное приложение  (wheel и sdist) появится в папке `dist/`

```bash
uv build
uv pip install dist/halter-0.1.2-py3-none-any.whl[cli]
```

---

## ⚙️ Версионирование

```bash
# numeric bump
uv version --bump patch
uv version --bump minor
uv version --bump major

# pre-release
uv version --bump alpha
uv version --bump beta
uv version --bump rc
```

---

## 📤 Публикация на TestPyPI и PyPI

### TestPyPI

> Убедитесь, что версия уникальна и правильный classifier для Dev Status.

1. Получите API-токен на [TestPyPI](https://test.pypi.org/manage/account/).
2. Публикация:

```bash
uv publish --index testpypi -t <токен>
```

> <токен> будет ввида `pypi-XXXXXX`

(Опционально) Чтобы не вводить, каждый раз токен при публикации, можно экспортировать его в переменные окружения:

```bash
export PYPI_TOKEN=<токен>   # Linux/macOS
setx PYPI_TOKEN <токен>     # Windows
```
