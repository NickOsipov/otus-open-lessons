---
name: new-lesson
description: >-
  Creates a new OTUS open lesson under courses/{Program}/{Program}-{YYYY-MM}/
  with README.md plus required Markdown presentation.md and practice.md
  (tracked in git) and optional uv demo in artifacts/code/.
  Programs are an open set: create a new courses/{Program}/ folder when the user
  names a course that is not there yet (for example AgentOps). Use when the user
  asks to create a new open lesson, новый урок, новый курс, анонс вебинара,
  presentation.md, practice.md, or scaffolding for any OTUS program including
  MLOps, DE, ML-Basic, ML-Special, LLM-DD, AI-ML-PM, AgentOps.
---

# New lesson

Создаёт открытый урок OTUS по правилам репозитория. Канон - корневой `AGENTS.md`.

## Что собрать до записи файлов

Нужны: программа, дата группы `YYYY-MM`, тема.

Программы - открытый список. Смотри существующие папки в `courses/` (`MLOps`, `DE`, `ML-Basic`, `ML-Special`, `LLM-DD`, `AI-ML-PM` и любые новые). Если курса ещё нет (например `AgentOps`) - создай `courses/{Program}/` и первый урок внутри. Не мапь новый курс на старый префикс.

Если чего-то нет - спроси. Не выдумывай программу и месяц. Если папка `courses/{Program}/{Program}-{YYYY-MM}/` уже есть - остановись и уточни.

Всегда создавай: `README.md`, `presentation.md`, `practice.md` (эти три в git). Код - в `artifacts/code/`, если на занятии есть команды или скрипты.

## Порядок действий

1. Если программа уже есть - прочитай 1-2 README соседних уроков (`courses/{Program}/`) и скопируй тон (эмодзи в заголовках - только если они уже есть у соседей). Если программа новая - используй шаблон без эмодзи, пока пользователь не попросил иначе.
2. Создай `courses/{Program}/{Program}-{YYYY-MM}/`.
3. Запиши `README.md`, `presentation.md` и `practice.md` по [templates.md](templates.md). Язык - русский. Не делай `.pptx` / PDF / HTML. Нигде не ставь длинное или среднее тире, только `-`.
4. Если нужна исполняемая практика - код только в `artifacts/code/`. Пиши `pyproject.toml` с `requires-python = "==3.12.8"`. Не создавай `.venv` (`uv venv` запрещён). Зависимости и запуск: `uv add` / `uv run`. Облако Yandex Cloud. Секреты в `.env`, не в git. Слайд «Практика», `practice.md` и `code/` должны описывать один и тот же план.
5. Python: все импорты и модульные переменные в начале файла, не внутри функций и классов. Module docstring:

```python
"""Module: {имя}
Description: {коротко, но емко}.
"""
```

   У каждой функции - docstring и type hints.
6. Не копируй `courses/LLM-DD/LLM-DD-2026-09/README.md` как шаблон. Не копируй старый `AI-ML-PM-2026-10/presentation.md` как формат слайдов.
7. Не коммить, пока пользователь явно не попросил. Сообщение: `feat({Program}): {Program}-{YYYY-MM} open lesson`.

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

Коротко скажи пути: README, `presentation.md`, `practice.md`, и `artifacts/code/`, если он есть.
