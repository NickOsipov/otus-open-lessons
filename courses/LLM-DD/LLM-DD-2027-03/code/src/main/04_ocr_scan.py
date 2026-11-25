"""Module: 04_ocr_scan
Description: Распознать PNG-страницы через vision-модель OpenAI, сохранить текст рядом с картинкой и проверить ключевые поля.
"""

from config.variables import OCR_DIR
from src.lib.demo_pdf import SCAN_KEY_FIELDS, scan_source_text
from src.lib.llm_client import ocr_page_image
from src.utils.text import similarity


def check_key_fields(text: str) -> list[str]:
    """Вернуть ключевые поля, которых нет в распознанном тексте."""
    return [field for field in SCAN_KEY_FIELDS if field not in text]


def ocr_scans() -> None:
    """Распознать страницы, для которых еще нет .txt, и напечатать результат проверки."""
    png_paths = sorted(OCR_DIR.glob("page_*.png"))
    if not png_paths:
        print("PNG-страниц нет: сначала запустите 03_render_scan.py")
        return
    for png_path in png_paths:
        txt_path = png_path.with_suffix(".txt")
        if txt_path.exists():
            print(f"{txt_path.name}: уже распознано, вызов API не делаем")
            continue
        text = ocr_page_image(png_path.read_bytes())
        txt_path.write_text(text, encoding="utf-8")
        score = similarity(text, scan_source_text())
        missing = check_key_fields(text)
        print(f"{txt_path.name}: {len(text)} chars, совпадение с эталоном демо: {score:.0%}")
        print(f"ключевые поля не найдены: {', '.join(missing) or 'нет'}")
        print(f"--- OCR text ---\n{text}\n---")


if __name__ == "__main__":
    ocr_scans()
