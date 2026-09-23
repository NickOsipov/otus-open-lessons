"""Module: embeddings
Description: Кодирование документов и запросов моделью multilingual-e5-small.
"""

from fastembed import TextEmbedding

from config import EMBEDDING_MODEL

_MODEL: TextEmbedding | None = None


def get_model() -> TextEmbedding:
    """Вернуть общую модель эмбеддингов для скриптов занятия."""
    global _MODEL
    if _MODEL is None:
        _MODEL = TextEmbedding(model_name=EMBEDDING_MODEL)
    return _MODEL


def embed_passages(texts: list[str]) -> list[list[float]]:
    """Построить векторы документов с префиксом passage для e5."""
    prefixed = [f"passage: {text}" for text in texts]
    return [vector.tolist() for vector in get_model().embed(prefixed)]


def embed_query(text: str) -> list[float]:
    """Построить вектор поискового запроса с префиксом query для e5."""
    vectors = list(get_model().query_embed([text]))
    return vectors[0].tolist()
