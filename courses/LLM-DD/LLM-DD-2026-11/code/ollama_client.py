"""Module: ollama_client
Description: Клиент Ollama через официальный OpenAI SDK.
"""

from openai import OpenAI

from config import OLLAMA_API_KEY, OLLAMA_BASE_URL, OLLAMA_MODEL

SYSTEM_PROMPT = (
    "Ты помощник магазина Орбита. Отвечай по-русски коротко. "
    "Используй только фрагменты из блока КОНТЕКСТ. "
    "Если ответа в контексте нет, так и скажи. Не выдумывай правила."
)


def build_llm_client() -> OpenAI:
    """Подключить OpenAI SDK к локальному OpenAI-совместимому API Ollama."""
    return OpenAI(
        api_key=OLLAMA_API_KEY,
        base_url=OLLAMA_BASE_URL,
    )


def answer_from_context(question: str, context: str) -> str:
    """Сгенерировать ответ модели только по переданному контексту."""
    user_content = f"КОНТЕКСТ:\n{context}\n\nВОПРОС: {question}"
    completion = build_llm_client().chat.completions.create(
        model=OLLAMA_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )
    message = completion.choices[0].message.content
    if message is None:
        return ""
    return message.strip()
