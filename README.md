# Halter

![Tests](https://github.com/<user>/<repo>/actions/workflows/tests.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/<user>/<repo>?logo=codecov)
![License](https://img.shields.io/github/license/<user>/<repo>)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)

## Описание

Приложение Halter — мультиплатформенный GUI на базе Flet. Позволяет структурировать сети и устройства, хранит проекты в формате YAML, поддерживает работу как в десктопном, так и в веб-режиме.

---

## Запуск приложения

### Через uv (универсальный запуск)

* Запуск десктопного приложения:

```bash
uv run flet run
```

* Запуск веб-приложения:

```bash
uv run flet run --web
```

Для подробностей смотрите [Getting Started Guide](https://flet.dev/docs/getting-started/).

---

## Сборка приложения

### Android

```bash
uv run flet build apk -v
```

Подробнее о сборке и подписывании `.apk` и `.aab`: [Android Packaging Guide](https://flet.dev/docs/publish/android/).

---

### iOS

```bash
uv run flet build ipa -v
```

Подробнее о сборке и подписывании `.ipa`: [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

---

### macOS

```bash
uv run flet build macos -v
```

Подробнее: [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

---

### Linux

```bash
uv run flet build linux -v
```

Подробнее: [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

---

### Windows

```bash
uv run flet build windows -v
```

Подробнее: [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).

---

## Разработка

* Клонируйте репозиторий и установите зависимости.

* Запускайте приложение локально через uv (см. раздел Запуск).

* Код написан на Python 3.13, используется Flet и современный стек библиотек.

---

## Тестирование

* Для запуска тестов используется `pytest`.

* Запустить все тесты можно командой:

```bash
uv run pytest
```

* Для проверки покрытия кода используйте:

```bash
uv run pytest --cov=src --cov-report=term-missing
```

* Рекомендуется покрывать тестами все ключевые модули и функции.

---

## Вклад

* Для новых функций создавайте отдельные ветки.

* Пишите понятные и лаконичные коммиты.

* Добавляйте тесты для новых возможностей и багфиксов.

* Перед отправкой пулл-реквеста убедитесь, что все тесты проходят.

---

## Контакты и поддержка

* Вопросы и предложения направляйте в issue или на почту проекта.

* Для обсуждения используйте соответствующие каналы связи.

---

Если хочешь, могу помочь с шаблоном CONTRIBUTING.md или с документацией API.

---
