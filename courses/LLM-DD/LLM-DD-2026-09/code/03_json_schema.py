"""Module: 03_json_schema
Description: Получает schema-constrained ответ и проверяет его через Pydantic.
"""

from models import TicketClassification
from yandex_client import OutputMode, generate

TICKET = (
    "С карты дважды списали оплату за сентябрь. "
    "Верните, пожалуйста, лишний платеж как можно быстрее."
)


def main() -> None:
    """Передать JSON Schema модели и вывести проверенный объект."""
    schema = TicketClassification.model_json_schema()
    raw_result = generate(TICKET, OutputMode.JSON_SCHEMA, schema)
    classification = TicketClassification.model_validate_json(raw_result)

    print(classification.model_dump_json(indent=2))
    print("\nКонтракт пройден")


if __name__ == "__main__":
    main()
