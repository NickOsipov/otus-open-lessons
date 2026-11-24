"""Module: 04_clean_pages
Description: Найти колонтитулы по правилу поле страницы плюс повтор и сравнить текст до и после очистки.
"""

import sys

import pymupdf

from config.variables import DEMO_PAGE, PDF_PATH
from src.lib.pdf_utils import clean_page_text, find_repeated_margin_texts


def compare_cleaning(page_number: int) -> None:
    """Напечатать найденные колонтитулы и текст страницы до и после очистки."""
    doc = pymupdf.open(PDF_PATH)
    repeated = find_repeated_margin_texts(doc)

    print("=== повторяющиеся тексты в полях страницы ===")
    for text in sorted(repeated):
        print(f"- {text}")

    page = doc[page_number - 1]
    print(f"\n=== page {page_number}: до очистки ===")
    print(page.get_text("text").strip())
    print(f"\n=== page {page_number}: после очистки ===")
    print(clean_page_text(page, repeated))
    doc.close()


if __name__ == "__main__":
    compare_cleaning(int(sys.argv[1]) if len(sys.argv) > 1 else DEMO_PAGE)
