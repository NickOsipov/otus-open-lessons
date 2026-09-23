"""Module: 04_filtered_search
Description: Поиск по сходству с фильтром shop/returns/year.
"""

from config import QUERY_TEXT
from filters import shop_returns_current_filter
from qdrant_utils import print_hits, search_knowledge


def search_with_filter() -> None:
    """Напечатать ближайшие документы среди актуальных правил возврата."""
    print(f"query: {QUERY_TEXT}")
    print_hits(
        "фильтр shop + returns + year >= 2025",
        search_knowledge(QUERY_TEXT, shop_returns_current_filter()),
    )


if __name__ == "__main__":
    search_with_filter()
