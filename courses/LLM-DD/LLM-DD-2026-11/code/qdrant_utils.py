"""Module: qdrant_utils
Description: Подключение к Qdrant, поиск по коллекции и печать выдачи.
"""

from collections.abc import Sequence

from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, ScoredPoint

from config import COLLECTION_NAME, QDRANT_URL, SEARCH_LIMIT
from embeddings import embed_query


def build_client() -> QdrantClient:
    """Создать клиент локального Qdrant."""
    return QdrantClient(url=QDRANT_URL)


def search_knowledge(
    query_text: str,
    query_filter: Filter | None = None,
    limit: int = SEARCH_LIMIT,
) -> list[ScoredPoint]:
    """Найти ближайшие документы с необязательным фильтром payload."""
    client = build_client()
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embed_query(query_text),
        query_filter=query_filter,
        limit=limit,
        with_payload=True,
    )
    return list(response.points)


def print_hits(title: str, hits: Sequence[ScoredPoint]) -> None:
    """Напечатать топ выдачи без сырых векторов."""
    print(title)
    if not hits:
        print("  пусто")
        return
    for index, hit in enumerate(hits, start=1):
        payload = hit.payload or {}
        score = round(float(hit.score), 4)
        print(
            f"  {index}. score={score} id={hit.id} "
            f"[{payload.get('department')}/{payload.get('doc_type')}/{payload.get('year')}] "
            f"{payload.get('title')}"
        )
