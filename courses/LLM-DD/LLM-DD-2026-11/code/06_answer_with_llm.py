"""Module: 06_answer_with_llm
Description: Сравнить ответы Ollama на одном запросе с разным контекстом из Qdrant.
"""

from collections.abc import Sequence

from qdrant_client.http.models import ScoredPoint

from config import OLLAMA_MODEL, QUERY_TEXT
from filters import shop_returns_current_filter
from ollama_client import answer_from_context
from qdrant_utils import print_hits, search_knowledge


def format_context(hits: Sequence[ScoredPoint]) -> str:
    """Собрать текст фрагментов для промпта модели."""
    if not hits:
        return "Документы не найдены."
    chunks: list[str] = []
    for hit in hits:
        payload = hit.payload or {}
        title = payload.get("title", "")
        text = payload.get("text", "")
        meta = (
            f"{payload.get('department')}/{payload.get('doc_type')}/"
            f"{payload.get('year')}"
        )
        chunks.append(f"[{meta}] {title}\n{text}")
    return "\n\n".join(chunks)


def print_answer(title: str, hits: Sequence[ScoredPoint]) -> None:
    """Показать найденный контекст и ответ llama3.2:3b."""
    print_hits(title, hits)
    print(f"модель: {OLLAMA_MODEL}")
    print(answer_from_context(QUERY_TEXT, format_context(hits)))
    print()


def compare_answers() -> None:
    """Сравнить генерацию без фильтра и с фильтром актуальных возвратов."""
    print(f"query: {QUERY_TEXT}")
    print_answer("без фильтра", search_knowledge(QUERY_TEXT))
    print_answer(
        "фильтр shop + returns + year >= 2025",
        search_knowledge(QUERY_TEXT, shop_returns_current_filter()),
    )


if __name__ == "__main__":
    compare_answers()
