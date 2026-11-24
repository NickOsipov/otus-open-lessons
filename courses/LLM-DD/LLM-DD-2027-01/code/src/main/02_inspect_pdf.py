"""Module: 02_inspect_pdf
Description: Осмотреть PDF: метаданные, размер страниц, длину текстового слоя и картинки.
"""

import pymupdf

from config.variables import PDF_PATH
from src.lib.pdf_utils import has_text_layer


def inspect_pdf() -> None:
    """Напечатать сводку по каждой странице и пометить страницы без текстового слоя."""
    doc = pymupdf.open(PDF_PATH)
    print(f"file: {PDF_PATH.name}")
    print(f"title: {doc.metadata.get('title')}")
    print(f"pages: {doc.page_count}")
    print()
    print(f"{'page':>4} | {'size':>11} | {'chars':>5} | {'images':>6} | verdict")
    for index, page in enumerate(doc):
        chars = len(page.get_text("text").strip())
        images = len(page.get_images())
        size = f"{page.rect.width:.0f}x{page.rect.height:.0f}"
        verdict = "текст" if has_text_layer(page) else "скан, нужен OCR"
        print(f"{index + 1:>4} | {size:>11} | {chars:>5} | {images:>6} | {verdict}")
    doc.close()


if __name__ == "__main__":
    inspect_pdf()
