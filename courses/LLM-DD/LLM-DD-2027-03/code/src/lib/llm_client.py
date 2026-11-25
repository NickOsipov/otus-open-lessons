"""Module: llm_client
Description: Клиент OpenAI API через официальный SDK: OCR картинки страницы и ответ модели по тексту страницы.
"""

import base64

from openai import OpenAI

from config.variables import OPENAI_API_KEY, OPENAI_MODEL

OCR_PROMPT = (
    "Распознай весь текст на изображении страницы документа. "
    "Верни только текст в том порядке, в котором он идет на странице. "
    "Цифры, серийные номера и даты переписывай точно. "
    "Не добавляй пояснений и не пересказывай."
)
SYSTEM_PROMPT = (
    "Ты помощник интернет-магазина. Отвечай по-русски коротко. "
    "Используй только текст из блока СТРАНИЦА и в конце укажи источник в виде (файл, стр. N). "
    "Если ответа на странице нет, ответь: нет в документе."
)


def build_llm_client() -> OpenAI:
    """Создать клиент OpenAI API с ключом из .env."""
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY не задан: скопируйте .env.example в .env и впишите ключ")
    return OpenAI(api_key=OPENAI_API_KEY)


def ocr_page_image(png: bytes) -> str:
    """Распознать текст на картинке страницы через vision-модель OpenAI."""
    encoded = base64.b64encode(png).decode("ascii")
    completion = build_llm_client().chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": OCR_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encoded}"},
                    },
                ],
            }
        ],
    )
    return (completion.choices[0].message.content or "").strip()


def answer_from_page(question: str, file_name: str, page_number: int, page_text: str) -> str:
    """Сгенерировать ответ только по тексту переданной страницы."""
    user_content = f"СТРАНИЦА ({file_name}, стр. {page_number}):\n{page_text}\n\nВОПРОС: {question}"
    completion = build_llm_client().chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )
    return (completion.choices[0].message.content or "").strip()
