"""Module: 05_compare
Description: Сравнить выдачу одного запроса с фильтром и без него.
"""

from config import QUERY_TEXT
from filters import shop_returns_current_filter
from qdrant_utils import print_hits, search_knowledge


def compare_searches() -> None:
    """Показать, как фильтр меняет топ для одного и того же запроса."""
    print(f"query: {QUERY_TEXT}")
    print_hits("без фильтра", search_knowledge(QUERY_TEXT))
    print_hits(
        "фильтр shop + returns + year >= 2025",
        search_knowledge(QUERY_TEXT, shop_returns_current_filter()),
    )


if __name__ == "__main__":
    compare_searches()
