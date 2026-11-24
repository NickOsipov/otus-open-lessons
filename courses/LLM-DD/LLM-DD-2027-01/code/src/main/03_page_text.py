"""Module: 03_page_text
Description: Показать текст одной страницы целиком и по блокам с координатами.
"""

import sys

import pymupdf

from config.variables import DEMO_PAGE, PDF_PATH
from src.lib.pdf_utils import text_blocks


def show_page(page_number: int) -> None:
    """Напечатать сырой текст страницы и ее текстовые блоки с координатами."""
    doc = pymupdf.open(PDF_PATH)
    page = doc[page_number - 1]

    print(f"=== page {page_number}: get_text('text') ===")
    print(page.get_text("text"))

    print(f"=== page {page_number}: get_text('blocks', sort=True) ===")
    print(f"page height: {page.rect.height:.0f}")
    for block in text_blocks(page):
        x0, y0, x1, y1, text = block[:5]
        preview = " ".join(text.split())[:70]
        print(f"y0={y0:6.1f} y1={y1:6.1f} x0={x0:5.1f} | {preview}")
    doc.close()


if __name__ == "__main__":
    show_page(int(sys.argv[1]) if len(sys.argv) > 1 else DEMO_PAGE)
