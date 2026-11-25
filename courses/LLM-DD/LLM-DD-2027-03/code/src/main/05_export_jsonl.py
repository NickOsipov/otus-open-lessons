"""Module: 05_export_jsonl
Description: Сохранить страницы PDF в JSONL: текст из текстового слоя или из OCR, с номером страницы и источником текста.
"""

import json

import pymupdf

from config.variables import OCR_DIR, PAGES_JSONL, PDF_PATH
from src.lib.pdf_utils import has_text_layer, page_text


def build_record(page: pymupdf.Page, index: int, file_name: str) -> dict:
    """Собрать запись страницы: текст из текстового слоя, из сохраненного OCR или пустой."""
    if has_text_layer(page):
        text, source = page_text(page), "text_layer"
    else:
        ocr_path = OCR_DIR / f"page_{index}.txt"
        if ocr_path.exists():
            text, source = ocr_path.read_text(encoding="utf-8").strip(), "ocr"
        else:
            text, source = "", "missing"
    return {
        "file": file_name,
        "page": index,
        "text": text,
        "chars": len(text),
        "source": source,
        "needs_ocr": source == "missing",
    }


def export_pages() -> None:
    """Записать по одной JSON-строке на страницу и напечатать сводку по источникам."""
    doc = pymupdf.open(PDF_PATH)
    records = [
        build_record(page, index, PDF_PATH.name) for index, page in enumerate(doc, start=1)
    ]
    doc.close()

    with PAGES_JSONL.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    for record in records:
        print(f"page {record['page']}: {record['chars']:>4} chars | {record['source']}")
    print(f"saved {len(records)} pages to {PAGES_JSONL.name}")


if __name__ == "__main__":
    export_pages()
