"""Module: 02_inspect_pdf
Description: Показать по страницам PDF количество символов, картинок и вердикт: есть ли текстовый слой или нужен OCR.
"""

import pymupdf

from config.variables import PDF_PATH
from src.lib.pdf_utils import has_text_layer, page_text


def inspect_pdf() -> None:
    """Напечатать по каждой странице символы, картинки и вердикт."""
    doc = pymupdf.open(PDF_PATH)
    print(f"document: {PDF_PATH.name}, pages: {doc.page_count}")
    for index, page in enumerate(doc, start=1):
        chars = len(page_text(page))
        images = len(page.get_images())
        verdict = "текст" if has_text_layer(page) else "скан, нужен OCR"
        print(f"page {index}: {chars:>4} chars | {images} img | {verdict}")
    doc.close()


if __name__ == "__main__":
    inspect_pdf()
