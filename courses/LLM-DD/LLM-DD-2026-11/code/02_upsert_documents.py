"""Module: 02_upsert_documents
Description: Закодировать корпус и загрузить точки в Qdrant.
"""

from qdrant_client.http import models

from config import COLLECTION_NAME
from documents import DOCUMENTS, passage_text
from embeddings import embed_passages
from qdrant_utils import build_client


def upsert_documents() -> None:
    """Отправить в коллекцию векторы документов вместе с payload."""
    client = build_client()
    texts = [passage_text(document) for document in DOCUMENTS]
    vectors = embed_passages(texts)
    points = [
        models.PointStruct(
            id=document["id"],
            vector=vector,
            payload={
                "title": document["title"],
                "text": document["text"],
                "department": document["department"],
                "doc_type": document["doc_type"],
                "year": document["year"],
            },
        )
        for document, vector in zip(DOCUMENTS, vectors, strict=True)
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"upserted {len(points)} points")


if __name__ == "__main__":
    upsert_documents()
