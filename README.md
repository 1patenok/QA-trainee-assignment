# QA Trainee Assignment

Решение тестового задания AvitoTech QA: задание 1 (баги по скриншотам) и задание 2.1 (API-автотесты).

Стенд: `https://qa-internship.avito.com`  
Стек: Python ≥ 3.9, pytest, requests, allure-pytest, ruff

## Артефакты задания

| Задание | Файл | Содержание |
|---------|------|------------|
| 1 | [BUGS.md](BUGS.md) (BUG-001 … BUG-031) | Баги по скриншотам |
| 2.1 | [TESTCASES.md](TESTCASES.md) | Тест-кейсы API |
| 2.1 | [BUGS.md](BUGS.md) (BUG-032 … BUG-040) | Баги API |
| 2.1 | `tests/`, `api/` | Автотесты |
| 2.1 | [reports/](reports/) | Пример Allure-отчёта |
| оба | [PROMPTS.md](PROMPTS.md) | Промпты для ИИ |

## Структура проекта

```
.
├── BUGS.md                 # баг-репорты (задание 1 и найденные дефекты API)
├── TESTCASES.md            # тест-кейсы API
├── PROMPTS.md              # промпты, использованные при работе с ИИ
├── requirements.txt        # зависимости
├── pyproject.toml          # pytest + ruff
├── reports/                # пример скриншотов Allure-отчёта
├── api/                    # клиент и обёртки над ручками (аналог Page Object)
│   ├── client.py           # HTTP + Allure step/attachments
│   ├── auth.py
│   ├── items.py
│   └── statistics.py
└── tests/                  # автотесты
    ├── conftest.py
    ├── helpers.py
    ├── test_register.py
    ├── test_auth.py
    ├── test_items.py
    ├── test_item_validation.py
    ├── test_access.py
    ├── test_statistics.py
    ├── test_delete.py
    ├── test_bugs.py        # известные баги (ожидаемо падают)
    ├── test_e2e.py
    └── test_nf.py
```

## Как запустить тесты

1. Склонируйте репозиторий (или скачайте ZIP и распакуйте).

2. Убедитесь, что установлен Python 3.9 или новее:

```bash
python3 --version
```

Если команды нет, установите Python с [официального сайта](https://www.python.org/downloads/). На Windows при установке включите опцию **Add python.exe to PATH**.

3. Перейдите в корневую директорию проекта (туда, где лежит `requirements.txt`):

```bash
cd /путь/до/проекта
```

4. Создайте виртуальное окружение:

```bash
python3 -m venv venv
```

5. Установите зависимости **через pip из venv**:

```bash
./venv/bin/pip install -r requirements.txt
```

На Windows: `venv\Scripts\pip install -r requirements.txt`

6. Запустите тесты **через pytest из venv**:

```bash
./venv/bin/pytest -v
```

На Windows: `venv\Scripts\pytest -v`

Дополнительная настройка не нужна: base URL стенда уже в коде.  
Результаты Allure пишутся в `allure-results/` (в `.gitignore`).

### Полезные команды

```bash
# только сценарии без известных багов
./venv/bin/pytest -v --ignore=tests/test_bugs.py

# один файл
./venv/bin/pytest -v tests/test_auth.py
```


## Allure-отчёт

В каждом HTTP-запросе есть Allure step и вложения `request` / `status_code` / `response_body`.  
У тестов заданы epic/feature; у E2E - отдельные шаги сценария.

1. Прогоните тесты (`./venv/bin/pytest -v`) - появится папка `allure-results/`.

2. Установите [Allure Commandline](https://docs.qameta.io/allure/#_installing_a_commandline) (если ещё нет), например:

```bash
npm install -g allure-commandline
```

3. Соберите и откройте отчёт:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Пример сформированного отчёта (полный прогон: 33 passed / 16 failed - известные баги в Known bugs):

- [reports/allure-overview.png](reports/allure-overview.png) - Overview
- [reports/allure-behaviors.png](reports/allure-behaviors.png) - Behaviors (epic API)

## Линтер и форматтер (ruff)

Правила зафиксированы в `pyproject.toml` (`[tool.ruff]`).

```bash
# проверка
ruff check api tests

# автоисправления
ruff check --fix api tests

# форматтер
ruff format api tests

# проверка форматирования без изменений
ruff format --check api tests
```

## Что ожидать от прогона

- Большая часть тестов должна проходить, если стенд доступен.
- Тесты в `tests/test_bugs.py` **намеренно падают**: они фиксируют дефекты API и ссылаются на `BUGS.md` (`BUG-032` … `BUG-040`).
- Стенд общий: под нагрузкой иногда возможны таймауты (например, HTTP 504). Повторите прогон через несколько минут.
