# Шаблоны нового урока

Не копируй `courses/LLM-DD/LLM-DD-2026-09/README.md`.

Ориентиры живых README (если программа уже есть): `courses/MLOps/MLOps-2026-03/README.md`, `courses/DE/DE-2026-02/README.md`, `courses/ML-Basic/ML-Basic-2026-01/README.md`. Для новой программы (например `AgentOps`) бери шаблон ниже, без эмодзи, пока у курса нет своего стиля.

Эмодзи в секциях ставь только если так оформлены соседние уроки той же программы.

Не используй `courses/AI-ML-PM/AI-ML-PM-2026-10/presentation.md` как шаблон слайдов.

## README.md

```markdown
# Тема: {название}

{1-3 предложения: боль аудитории и обещание урока}

## Что вас ждет на вебинаре?

1. ...
2. ...
3. ...

## Кому будет полезно?

- {роль}: {зачем}
- {роль}: {зачем}
- {роль}: {зачем}

## Что вы узнаете по итогам вебинара?

- Как ...
- Как ...
- Как ...
```

## presentation.md

Только Markdown. Слайды для показа, не полный конспект практики.

```markdown
# {название}

## Цели

После занятия вы сможете:

1. {короткое умение}
2. {короткое умение}
3. {короткое умение}

## Смысл занятия

{один ответ: для чего нам это уметь}

## Теория 1. {короткий заголовок}

{тезисы}

## Теория 2. {короткий заголовок}

{тезисы}

## Теория 3. {короткий заголовок}

{тезисы}

## Теория 4. {короткий заголовок}

{тезисы}

## Практика

План (совпадает с `practice.md` и `{lesson}/code/`):

1. {шаг}
2. {шаг}
3. {шаг}
```

Слайдов «Теория N» должно быть от 4 до 6. Целей - ровно три, коротких. Смысл занятия - ровно один.

## practice.md

Полный ход практики: все действия, команды, ожидаемый результат. Можно провести занятие, читая только этот файл.

Команды практики: `uv add`, `uv run`. Не `uv venv`, не `python -m venv`. Python в `pyproject.toml`: `requires-python = "==3.12.8"`.

В начале `practice.md` явно напиши выбранный бэкенд: Yandex Cloud (что нужно в каталоге/ключах) или Ollama (установка, `ollama pull`, локальный URL). Не описывай оба как равнозначный путь в одном уроке.

````markdown
# Практика: {название}

План совпадает со слайдом «Практика» в `presentation.md`.

## 1. {шаг}

```bash
{команда}
```

Ожидаемо: {что увидеть}.

## 2. {шаг}

{действие / путь к файлу в code/}

## 3. {шаг}

{действие}
````

## code/pyproject.toml

Файл пиши руками, не через `uv add`: любая команда uv без `UV_PROJECT_ENVIRONMENT` создаст `.venv` в папке урока и будет заблокирована хуком. Версия Python - строго 3.12.8.

```toml
[project]
name = "{lesson-slug}"
version = "0.1.0"
requires-python = "==3.12.8"
dependencies = []
```

## Раскладка code/

Всегда эти папки, даже если в одной из них один файл. Скрипты в корне `code/` не клади.

```
code/
  pyproject.toml
  .env.example
  config/__init__.py
  config/variables.py
  src/__init__.py
  src/lib/__init__.py
  src/lib/{предмет}.py
  src/main/__init__.py
  src/main/01_{шаг}.py
  src/utils/__init__.py
  src/utils/{помощник}.py
```

Запуск из `code/`:

```bash
PYTHONPATH=. uv run python src/main/01_{шаг}.py
```

## config/variables.py

Только константы и чтение `.env`. Пути строй от корня `code/`, не от текущей папки процесса.

```python
"""Module: variables
Description: Пути, пороги и настройки модели для занятия.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

CODE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = CODE_DIR / "data"
```

## src/main и src/lib

```python
"""Module: {имя}
Description: {коротко, но емко, зачем файл}.
"""

from config.variables import DATA_DIR
from src.lib.example import do_step


def main() -> None:
    """Коротко, что делает шаг практики."""
    print(do_step(DATA_DIR))


if __name__ == "__main__":
    main()
```

Импорты только сверху. Не импортируй внутри функций и классов. У каждой функции - docstring и type hints. В тексте только дефис `-`, без длинного тире. `src/utils` не импортирует `src.lib` и `config`.
