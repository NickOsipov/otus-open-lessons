"""Module: llm_client
Description: Ответ модели по одной странице PDF через официальный OpenAI SDK.
"""

from openai import OpenAI

from config.variables import OPENAI_API_KEY, OPENAI_MODEL

SYSTEM_PROMPT = (
    "Ты помощник магазина Орбита. Отвечай по-русски коротко. "
    "Используй только текст из блока СТРАНИЦА и в конце укажи источник в виде (файл, стр. N). "
    "Если ответа на странице нет, ответь: нет в документе."
)


def build_llm_client() -> OpenAI:
    """Создать клиент OpenAI API с ключом из .env."""
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY не задан: скопируйте .env.example в .env и впишите ключ")
    return OpenAI(api_key=OPENAI_API_KEY)


def answer_from_page(question: str, file_name: str, page_number: int, page_text: str) -> str:
    """Сгенерировать ответ только по тексту переданной страницы."""
    user_content = (
        f"СТРАНИЦА ({file_name}, стр. {page_number}):\n{page_text}\n\nВОПРОС: {question}"
    )
    completion = build_llm_client().chat.completions.create(
        model=OPENAI_MODEL,
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
