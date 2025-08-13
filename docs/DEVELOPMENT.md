# 🛠️ Разработка Halter

## 🔧 Разработка и установка

### 0. Подготовка среды разработки

Установка uv (<https://docs.astral.sh/uv/getting-started/installation/>)

Копирование репозитория и создание виртуального окружения.

```bash
git clone https://github.com/herokrat/halter.git
cd halter
uv venv
uv sync         # Устанавливает обычные зависимости
uv add --dev     # Устанавливает все dev-зависимости
```

---

## 🧪 Тестирование

```bash
pytest --cov
mypy src
ruff check src
mkdocs build
mkdocs server
```

либо использовать poe создать синонимы команд

```bash
poe test
poe check
poe format
poe docs
poe docs-test
```

---

## 📦 Сборка wheel и sdist

```bash
uv build
# wheel и sdist появятся в dist/
# локально установить вот так
uv pip install dist/halter-0.1.2-py3-none-any.whl[cli]
```

---

## 📤 Публикация на TestPyPI и PyPI

### TestPyPI

1. Получите API-токен на [TestPyPI](https://test.pypi.org/manage/account/).
2. Экспортируйте его в переменные окружения:

```bash
export PYPI_TOKEN=<токен>   # Linux/macOS
setx PYPI_TOKEN <токен>    # Windows
```

3. Публикация:

```bash
uv publish --index testpypi -t САМ_ТОКЕН
```

### PyPI (после тестирования)

```bash
twine upload dist/*
```

> Убедитесь, что версия уникальна и правильный classifier для Dev Status.

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
