"""Module: 01_make_pdf
Description: Собрать учебный PDF интернет-магазина: четыре страницы с текстовым слоем и страница-скан из одной картинки.
"""

import pymupdf

from config.variables import DATA_DIR, PDF_PATH
from src.lib.demo_pdf import (
    PAGE_HEIGHT,
    PAGE_WIDTH,
    PAGES,
    TEXT_STYLE,
    TOTAL_PAGES,
    draw_page,
    make_scan_image,
)


def build_pdf() -> None:
    """Собрать PDF: текстовые страницы и страница, в которой есть только картинка."""
    DATA_DIR.mkdir(exist_ok=True)
    doc = pymupdf.open()
    doc.set_metadata({"title": "Руководство покупателя интернет-магазина", "author": "Интернет-магазин"})

    for number, (title, body) in enumerate(PAGES, start=1):
        page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        draw_page(page, title, body, number, TEXT_STYLE)

    scan = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    scan.insert_image(scan.rect, stream=make_scan_image())

    doc.save(PDF_PATH)
    doc.close()
    print(f"saved {PDF_PATH.name}: {TOTAL_PAGES} pages")


if __name__ == "__main__":
    build_pdf()
