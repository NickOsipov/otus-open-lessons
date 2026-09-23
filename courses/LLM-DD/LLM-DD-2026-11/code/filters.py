"""Module: filters
Description: Фильтр payload для актуальных правил возврата магазина.
"""

from qdrant_client.http import models


def shop_returns_current_filter() -> models.Filter:
    """Оставить только актуальные правила возврата товара."""
    return models.Filter(
        must=[
            models.FieldCondition(
                key="department",
                match=models.MatchValue(value="shop"),
            ),
            models.FieldCondition(
                key="doc_type",
                match=models.MatchValue(value="returns"),
            ),
            models.FieldCondition(
                key="year",
                range=models.Range(gte=2025),
            ),
        ]
    )
