"""Module: yandex_client
Description: Вызывает Yandex AI Studio через OpenAI SDK в трех режимах формата ответа.
"""

import os
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

BASE_URL = "https://ai.api.cloud.yandex.net/v1"
SCHEMA_NAME = "ticket_classification"
SYSTEM_PROMPT = (
    "Ты классифицируешь обращения в поддержку. "
    "Отвечай на русском языке и не добавляй факты, которых нет в обращении."
)
JSON_OBJECT_HINT = (
    " Верни только JSON-объект с полями category, priority, summary, "
    "requires_human. Допустимые category: billing, bug, feature, access, other. "
    "Допустимые priority: low, medium, high, critical."
)


class OutputMode(StrEnum):
    """Режим форматирования ответа модели."""

    TEXT = "text"
    JSON_OBJECT = "json_object"
    JSON_SCHEMA = "json_schema"


@dataclass(frozen=True)
class Settings:
    """Настройки подключения к Yandex AI Studio."""

    api_key: str
    folder_id: str
    model_uri: str
    base_url: str


def load_settings() -> Settings:
    """Загрузить настройки из переменных окружения или файла .env."""
    load_dotenv()
    api_key = os.getenv("YC_API_KEY", "")
    folder_id = os.getenv("YC_FOLDER_ID", "")
    model_uri = os.getenv("YC_MODEL_URI", "")
    base_url = os.getenv("YC_BASE_URL", BASE_URL)

    if not api_key or not folder_id:
        raise RuntimeError("Заполните YC_API_KEY и YC_FOLDER_ID в файле .env")
    if not model_uri:
        model_uri = f"gpt://{folder_id}/yandexgpt/latest"

    return Settings(
        api_key=api_key,
        folder_id=folder_id,
        model_uri=model_uri,
        base_url=base_url,
    )


def build_client(settings: Settings) -> OpenAI:
    """Создать клиент OpenAI SDK, направленный в Yandex AI Studio."""
    return OpenAI(
        api_key=settings.api_key,
        base_url=settings.base_url,
        project=settings.folder_id,
        timeout=30.0,
    )


def build_response_format(
    mode: OutputMode,
    schema: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Собрать параметр response_format для выбранного режима вывода."""
    if mode is OutputMode.TEXT:
        return None
    if mode is OutputMode.JSON_OBJECT:
        return {"type": "json_object"}
    if schema is None:
        raise ValueError("Для режима JSON Schema необходимо передать схему")
    return {
        "type": "json_schema",
        "json_schema": {"name": SCHEMA_NAME, "schema": schema},
    }


def build_messages(ticket: str, mode: OutputMode) -> list[dict[str, str]]:
    """Собрать сообщения запроса с учетом режима вывода."""
    system_prompt = SYSTEM_PROMPT
    if mode is OutputMode.JSON_OBJECT:
        system_prompt += JSON_OBJECT_HINT

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": ticket},
    ]


def generate(
    ticket: str,
    mode: OutputMode,
    schema: dict[str, Any] | None = None,
) -> str:
    """Отправить обращение модели и вернуть сгенерированный текст."""
    settings = load_settings()
    client = build_client(settings)
    response_format = build_response_format(mode, schema)

    extra: dict[str, Any] = {}
    if response_format is not None:
        extra["response_format"] = response_format

    completion = client.chat.completions.create(
        model=settings.model_uri,
        messages=build_messages(ticket, mode),
        temperature=0,
        max_tokens=500,
        **extra,
    )
    content = completion.choices[0].message.content

    if not content:
        raise RuntimeError("Модель вернула пустой ответ")

    return content
