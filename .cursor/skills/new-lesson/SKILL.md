---
name: new-lesson
description: >-
  Creates a new OTUS open lesson under courses/{Program}/{Program}-{YYYY-MM}/
  with README.md plus required Markdown presentation.md and practice.md
  (tracked in git) and optional uv demo in {lesson}/code/.
  Programs are an open set: create a new courses/{Program}/ folder when the user
  names a course that is not there yet (for example AgentOps). Use when the user
  asks to create a new open lesson, новый урок, новый курс, анонс вебинара,
  presentation.md, practice.md, or scaffolding for any OTUS program including
  MLOps, DE, ML-Basic, ML-Special, LLM-DD, AI-ML-PM, AgentOps.
---

# New lesson

Создаёт открытый урок OTUS по правилам репозитория. Канон - корневой `AGENTS.md`.

## Что собрать до записи файлов

Нужны: программа, дата группы `YYYY-MM`, тема, **бэкенд практики**.

Бэкенд практики - ровно один из двух: **Yandex Cloud** или **локальная Ollama**. Спроси явно, если пользователь ещё не назвал. Не выбирай сам, не пиши файлы до ответа, не смешивай оба в одном уроке без просьбы. AWS, GCP, Azure и чужие API моделей не подставляй.

Программы - открытый список. Смотри существующие папки в `courses/` (`MLOps`, `DE`, `ML-Basic`, `ML-Special`, `LLM-DD`, `AI-ML-PM` и любые новые). Если курса ещё нет (например `AgentOps`) - создай `courses/{Program}/` и первый урок внутри. Не мапь новый курс на старый префикс.

Если чего-то нет - спроси. Не выдумывай программу и месяц. Если папка `courses/{Program}/{Program}-{YYYY-MM}/` уже есть - остановись и уточни.

Всегда создавай: `README.md`, `presentation.md`, `practice.md` (эти три в git). Код - в `{lesson}/code/`, если на занятии есть команды или скрипты.

## Порядок действий

1. Если программа уже есть - прочитай 1-2 README соседних уроков (`courses/{Program}/`) и скопируй тон (эмодзи в заголовках - только если они уже есть у соседей). Если программа новая - используй шаблон без эмодзи, пока пользователь не попросил иначе.
2. Создай `courses/{Program}/{Program}-{YYYY-MM}/`.
3. Запиши `README.md`, `presentation.md` и `practice.md` по [templates.md](templates.md). Язык - русский. Не делай `.pptx` / PDF / HTML. Нигде не ставь длинное или среднее тире, только `-`.
4. Если нужна исполняемая практика - код только в `{lesson}/code/` и только в раскладке из раздела «Структура code/» ниже. Скрипты в корне `code/` не клади. Пиши `pyproject.toml` с `requires-python = "==3.12.8"` руками, зависимости перечисляй сам. Все обращения к LLM - через **OpenAI SDK** (пакет `openai`), см. раздел ниже. При создании урока ничего не устанавливай: `uv venv`, `uv add`, `uv sync`, `uv run` без `UV_PROJECT_ENVIRONMENT` создают `.venv` в папке урока и блокируются хуком `.cursor/hooks/no-venv.sh`. Нужен реальный прогон - только так: `UV_PROJECT_ENVIRONMENT="$HOME/.cache/otus-uv/{Program}-{YYYY-MM}" uv run ...`. В `practice.md` для студентов остаются обычные `uv add` / `uv run`; скрипты запускаются как `PYTHONPATH=. uv run python src/main/...`. Практика - выбранный бэкенд (Yandex Cloud или Ollama). Секреты в `.env`, не в git. Слайд «Практика», `practice.md` и `code/` должны описывать один и тот же план.
5. Python: все импорты и модульные переменные в начале файла, не внутри функций и классов. Module docstring:

```python
"""Module: {имя}
Description: {коротко, но емко}.
"""
```

   У каждой функции - docstring и type hints.
6. Не копируй `courses/LLM-DD/LLM-DD-2026-09/README.md` как шаблон. Не копируй старый `AI-ML-PM-2026-10/presentation.md` как формат слайдов.
7. Не коммить, пока пользователь явно не попросил. Сообщение: `feat({Program}): {Program}-{YYYY-MM} open lesson`.

## Структура code/

Код занятия всегда раскладывай так, даже если какая-то папка почти пустая. Плоский набор `*.py` в корне `code/` не используй.

```
{lesson}/code/
  pyproject.toml
  .env.example
  config/variables.py    # константы, пути, пороги, имена моделей, чтение .env
  src/lib/               # предметная логика занятия
  src/main/              # точки входа, по файлу на шаг практики
  src/utils/             # мелкие помощники без предметной логики
```

- `config/variables.py` - только настройки. Функции предметной логики сюда не клади.
- `src/lib/` - то, ради чего урок: разбор документа, клиент модели, работа с индексом.
- `src/main/` - запускаемые шаги. Имена можно нумеровать: `01_....py`, `02_....py`. Один шаг практики - один файл.
- `src/utils/` - общие куски без знания задачи: нормализация строки, разбор слов.
- Импорты: `src/main` берет `src.lib`, `src.utils` и `config.variables`. `src.lib` может брать `src.utils` и `config.variables`. `src.utils` не импортирует `src.lib` и `config`.
- В папках `config`, `src`, `src/lib`, `src/main`, `src/utils` есть `__init__.py` с module docstring.
- Запуск из `{lesson}/code/`: `PYTHONPATH=. uv run python src/main/01_example.py`. `PYTHONPATH=.` обязателен: файл лежит не в корне `code/`, а импорты идут от этого корня (`config`, `src`).
- В `practice.md` команды и пути к файлам совпадают с этой раскладкой.

## Вызовы LLM: только OpenAI SDK

Любой код урока, который обращается к языковой модели, использует официальный **OpenAI SDK** (`openai`). Не пиши ручные HTTP-запросы через `httpx`, `requests` или `curl` к нативному REST API модели и не тащи `yandex-cloud-ml-sdk`, пока пользователь явно не попросил.

Бэкенд уже должен быть выбран пользователем. SDK один, отличаются `base_url`, ключ и имя модели.

**Yandex AI Studio** (если выбрали Yandex Cloud):

```python
from openai import OpenAI

client = OpenAI(
    api_key=api_key,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=folder_id,
)
completion = client.chat.completions.create(
    model=f"gpt://{folder_id}/yandexgpt/latest",
    messages=[{"role": "user", "content": prompt}],
)
```

Ключ и `folder_id` только из `.env`.

**Ollama** (если выбрали локальную модель):

```python
from openai import OpenAI

client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1",
)
completion = client.chat.completions.create(
    model="llama3.2:3b",
    messages=[{"role": "user", "content": prompt}],
)
```

`api_key="ollama"` - заглушка: SDK требует непустое поле, Ollama ключ не проверяет. Имя модели и `ollama pull` должны совпадать с `practice.md`. В практике облачный ключ Yandex Cloud не нужен.

- Structured Outputs задавай через `response_format`: `{"type": "json_object"}` или `{"type": "json_schema", "json_schema": {"name": ..., "schema": ...}}`.
- Схему бери из Pydantic через `model_json_schema()`, ответ проверяй обратно через `model_validate_json()`.
- Секреты только из `.env`, никогда в коде и логах.
- Ручной HTTP допустим лишь там, где у сервиса нет OpenAI-совместимого endpoint. Тогда напиши в `practice.md`, почему.

## README: жёсткие правила

- Конкретная тема, без «введение в ML».
- 3 пункта «что будет», 3 аудитории, 3 исхода (можно чуть больше, если урок того требует).
- Исходы - умения: «как настроить…», не «узнаете про…».
- Не обещать полный курс, сертификат, ДЗ. Формат - открытый урок ~50-90 минут.
- Практический тон, без канцелярита.

## Презентация: жёсткие правила

- Слайд «Цели»: ровно 3 коротких умения после занятия.
- Слайд «Смысл занятия»: ровно один ответ «для чего нам это уметь?».
- Слайды «Теория 1» … «Теория N»: от 4 до 6, не больше.
- Слайд «Практика»: только план, без полного конспекта команд - полный ход в `practice.md`.

## После создания

Коротко скажи пути: README, `presentation.md`, `practice.md`, и `{lesson}/code/`, если он есть.
