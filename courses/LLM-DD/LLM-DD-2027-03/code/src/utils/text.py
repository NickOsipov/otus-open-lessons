"""Module: text
Description: Грубые основы слов для поиска страницы и мера совпадения двух текстов для проверки OCR.
"""

import difflib
import re

STEM_LENGTH = 5
MIN_WORD_LENGTH = 4


def stems(text: str) -> set[str]:
    """Разбить текст на грубые основы слов: первые буквы снимают русские окончания."""
    words = re.findall(r"\w+", text.lower())
    return {word[:STEM_LENGTH] for word in words if len(word) >= MIN_WORD_LENGTH}


def similarity(first: str, second: str) -> float:
    """Вернуть долю совпадения двух текстов от 0 до 1, без учета регистра и лишних пробелов."""
    matcher = difflib.SequenceMatcher(
        None,
        " ".join(first.split()).lower(),
        " ".join(second.split()).lower(),
        autojunk=False,
    )
    return matcher.ratio()
