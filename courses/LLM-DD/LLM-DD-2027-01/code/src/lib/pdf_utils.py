"""Module: pdf_utils
Description: Блоки страницы PyMuPDF, поиск колонтитулов и извлечение очищенного текста по страницам.
"""

import math
from collections import Counter
from pathlib import Path

import pymupdf

from config.variables import MARGIN_PT, MIN_TEXT_CHARS, REPEAT_SHARE
from src.utils.text import normalize_text

Block = tuple[float, float, float, float, str, int, int]

TEXT_BLOCK_TYPE = 0


def text_blocks(page: pymupdf.Page) -> list[Block]:
    """Вернуть текстовые блоки страницы в порядке чтения сверху вниз."""
    blocks = page.get_text("blocks", sort=True)
    return [block for block in blocks if block[6] == TEXT_BLOCK_TYPE]


def is_in_margin(block: Block, page_height: float) -> bool:
    """Проверить, лежит ли блок целиком в верхнем или нижнем поле страницы."""
    y0, y1 = block[1], block[3]
    return y1 <= MARGIN_PT or y0 >= page_height - MARGIN_PT


def has_text_layer(page: pymupdf.Page) -> bool:
    """Проверить, есть ли у страницы текстовый слой."""
    return len(page.get_text("text").strip()) >= MIN_TEXT_CHARS


def find_repeated_margin_texts(doc: pymupdf.Document) -> set[str]:
    """Найти тексты из полей страницы, которые повторяются на большинстве страниц."""
    counter: Counter[str] = Counter()
    for page in doc:
        seen = {
            normalize_text(block[4])
            for block in text_blocks(page)
            if is_in_margin(block, page.rect.height)
        }
        counter.update(seen)
    min_pages = max(2, math.ceil(doc.page_count * REPEAT_SHARE))
    return {text for text, count in counter.items() if count >= min_pages}


def clean_page_text(page: pymupdf.Page, repeated: set[str]) -> str:
    """Собрать текст страницы без повторяющихся колонтитулов и номеров страниц."""
    parts = []
    for block in text_blocks(page):
        if is_in_margin(block, page.rect.height) and normalize_text(block[4]) in repeated:
            continue
        text = block[4].strip()
        if text:
            parts.append(text)
    return "\n".join(parts)


def extract_pages(pdf_path: Path) -> list[dict]:
    """Извлечь очищенный текст каждой страницы с номером и признаком скана."""
    doc = pymupdf.open(pdf_path)
    repeated = find_repeated_margin_texts(doc)
    records = []
    for index, page in enumerate(doc):
        text = clean_page_text(page, repeated)
        records.append(
            {
                "file": pdf_path.name,
                "page": index + 1,
                "text": text,
                "chars": len(text),
                "needs_ocr": not has_text_layer(page),
            }
        )
    doc.close()
    return records
