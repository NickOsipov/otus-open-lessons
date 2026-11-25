"""Module: variables
Description: Пути к данным урока, параметры рендера страниц и настройки OpenAI API.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

CODE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = CODE_DIR / "data"
OCR_DIR = DATA_DIR / "ocr"
PDF_PATH = DATA_DIR / "shop_manual.pdf"
PAGES_JSONL = DATA_DIR / "pages.jsonl"

MIN_TEXT_CHARS = 20
RENDER_DPI = 150

QUESTION = "Какой срок ремонта указан в акте приема устройства?"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
