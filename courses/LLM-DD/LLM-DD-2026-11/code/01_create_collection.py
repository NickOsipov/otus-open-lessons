"""Module: 01_create_collection
Description: Создать коллекцию Qdrant и индексы полей payload.
"""

from qdrant_client.http import models

from config import COLLECTION_NAME, DISTANCE, VECTOR_SIZE
from qdrant_utils import build_client


def reset_collection() -> None:
    """Пересоздать коллекцию и индексы department, doc_type, year."""
    client = build_client()
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=DISTANCE),
    )
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="department",
        field_schema=models.PayloadSchemaType.KEYWORD,
    )
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="doc_type",
        field_schema=models.PayloadSchemaType.KEYWORD,
    )
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="year",
        field_schema=models.PayloadSchemaType.INTEGER,
    )
    print(f"collection {COLLECTION_NAME} created")
    print("payload indexes: department, doc_type, year")


if __name__ == "__main__":
    reset_collection()
