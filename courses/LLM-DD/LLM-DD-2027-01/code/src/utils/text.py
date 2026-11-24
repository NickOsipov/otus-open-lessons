"""Module: text
Description: Нормализация строк и грубые основы слов для сравнения текста.
"""

import re

STEM_LENGTH = 5
MIN_WORD_LENGTH = 4


def normalize_text(text: str) -> str:
    """Схлопнуть пробелы и заменить цифры на #, чтобы номера страниц совпадали."""
    collapsed = " ".join(text.split())
    return re.sub(r"\d+", "#", collapsed)


def stems(text: str) -> set[str]:
    """Разбить текст на грубые основы слов: первые буквы снимают русские окончания."""
    words = re.findall(r"\w+", text.lower())
    return {word[:STEM_LENGTH] for word in words if len(word) >= MIN_WORD_LENGTH}
