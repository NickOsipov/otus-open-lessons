"""Module: 03_render_scan
Description: Отрисовать страницы без текстового слоя в PNG-файлы, чтобы передать их на OCR.
"""

import pymupdf

from config.variables import OCR_DIR, PDF_PATH, RENDER_DPI
from src.lib.pdf_utils import has_text_layer, render_page_png


def render_scans() -> None:
    """Сохранить PNG для каждой страницы без текстового слоя и напечатать результат."""
    OCR_DIR.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(PDF_PATH)
    rendered = 0
    for index, page in enumerate(doc, start=1):
        if has_text_layer(page):
            continue
        path = OCR_DIR / f"page_{index}.png"
        path.write_bytes(render_page_png(page, RENDER_DPI))
        print(f"saved {path.name}")
        rendered += 1
    doc.close()
    print(f"rendered {rendered} scan page(s)")


if __name__ == "__main__":
    render_scans()
