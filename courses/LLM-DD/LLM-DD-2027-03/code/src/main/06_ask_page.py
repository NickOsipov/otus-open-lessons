"""Module: 06_ask_page
Description: Найти страницу под вопрос по пересечению основ слов и получить ответ модели со ссылкой на страницу.
"""

import json
import sys

from config.variables import PAGES_JSONL, QUESTION
from src.lib.llm_client import answer_from_page
from src.utils.text import stems


def load_pages() -> list[dict]:
    """Прочитать страницы из JSONL."""
    with PAGES_JSONL.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def find_best_page(question: str, pages: list[dict]) -> tuple[dict | None, int]:
    """Выбрать страницу с текстом, у которой больше всего общих основ слов с вопросом."""
    question_stems = stems(question)
    best_page = None
    best_score = 0
    for page in pages:
        if not page["text"]:
            continue
        score = len(question_stems & stems(page["text"]))
        if score > best_score:
            best_page, best_score = page, score
    return best_page, best_score


def ask(question: str) -> None:
    """Напечатать найденную страницу и ответ модели по ней."""
    pages = load_pages()
    missing = [page["page"] for page in pages if page["needs_ocr"]]
    print(f"question: {question}")
    print(f"pages without text: {missing}")

    page, score = find_best_page(question, pages)
    if page is None:
        print("подходящей страницы с текстом нет")
        return

    print(f"best page: {page['file']}, стр. {page['page']}, source: {page['source']} (common stems: {score})")
    print(f"--- page text ---\n{page['text']}\n---")
    answer = answer_from_page(question, page["file"], page["page"], page["text"])
    print(f"answer: {answer}")


if __name__ == "__main__":
    ask(sys.argv[1] if len(sys.argv) > 1 else QUESTION)
