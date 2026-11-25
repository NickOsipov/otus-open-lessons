"""Module: pdf_utils
Description: Проверка текстового слоя страницы, извлечение текста и рендер страницы в PNG для OCR.
"""

import pymupdf

from config.variables import MIN_TEXT_CHARS


def page_text(page: pymupdf.Page) -> str:
    """Вернуть текст страницы из текстового слоя PDF."""
    return page.get_text("text").strip()


def has_text_layer(page: pymupdf.Page) -> bool:
    """Проверить, есть ли у страницы текстовый слой достаточной длины."""
    return len(page_text(page)) >= MIN_TEXT_CHARS


def render_page_png(page: pymupdf.Page, dpi: int) -> bytes:
    """Отрисовать страницу в PNG: так страница-скан попадает в vision-модель."""
    return page.get_pixmap(dpi=dpi).tobytes("png")
