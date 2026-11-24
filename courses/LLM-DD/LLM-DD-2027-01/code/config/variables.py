"""Module: variables
Description: Пути к учебному PDF, правила очистки страниц и настройки OpenAI API.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

CODE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = CODE_DIR / "data"
PDF_PATH = DATA_DIR / "orbita_manual.pdf"
PAGES_JSONL = DATA_DIR / "pages.jsonl"

MARGIN_PT = 50.0
REPEAT_SHARE = 0.6
MIN_TEXT_CHARS = 20
DEMO_PAGE = 3

QUESTION = "Сколько месяцев действует гарантия на ремонт и куда сдать устройство?"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
