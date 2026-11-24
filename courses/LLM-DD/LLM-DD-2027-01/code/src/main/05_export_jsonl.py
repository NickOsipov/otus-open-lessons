"""Module: 05_export_jsonl
Description: Сохранить очищенные страницы PDF в JSONL с номером страницы и признаком скана.
"""

import json

from config.variables import PAGES_JSONL, PDF_PATH
from src.lib.pdf_utils import extract_pages


def export_pages() -> None:
    """Записать по одной JSON-строке на страницу и напечатать сводку."""
    records = extract_pages(PDF_PATH)
    with PAGES_JSONL.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    for record in records:
        flag = "needs_ocr" if record["needs_ocr"] else "ok"
        print(f"page {record['page']}: {record['chars']:>4} chars | {flag}")
    print(f"saved {len(records)} pages to {PAGES_JSONL.name}")


if __name__ == "__main__":
    export_pages()
