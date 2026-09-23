"""Module: 03_plain_search
Description: Поиск по сходству без фильтра по метаданным.
"""

from config import QUERY_TEXT
from qdrant_utils import print_hits, search_knowledge


def search_without_filter() -> None:
    """Напечатать ближайшие документы только по вектору запроса."""
    print(f"query: {QUERY_TEXT}")
    print_hits("без фильтра", search_knowledge(QUERY_TEXT))


if __name__ == "__main__":
    search_without_filter()
