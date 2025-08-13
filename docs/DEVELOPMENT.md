# 🛠️ Разработка Halter

## 🔧 Разработка и установка

### 1. Установка напрямую из PyPI

```bash
pip install halter[cli]       # CLI
pip install halter[gui]       # GUI
pip install halter             # Полная установка
````

### 2. Установка из TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ halter[cli]
pip install --index-url https://test.pypi.org/simple/ halter[gui]
pip install --index-url https://test.pypi.org/simple/ halter
```

> Используется для проверки pre-release версий.

---

## 🧪 Тестирование

```bash
pytest --cov
mypy src
ruff check src
```

---

## 📦 Сборка wheel и sdist

```bash
python -m build
# wheel и sdist появятся в dist/
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
twine upload --repository testpypi dist/*
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

---

## 🧹 Линтинг и форматирование

```bash
ruff check src
black src
isort src
```

---

## ⚠️ Советы

* Для проверки локально:

```bash
python -c "import halter; print(halter.__file__)"
```

* Для `flet` игнорируем mypy предупреждения:

```toml
[tool.mypy-flet.*]
ignore_missing_imports = true
```

* Для предупреждения о hardlink при сборке wheel:

```bash
export UV_LINK_MODE=copy   # Linux/macOS
set UV_LINK_MODE=copy      # Windows
```
