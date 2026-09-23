"""Module: 01_unstructured
Description: Демонстрирует свободный текстовый ответ без гарантий формата.
"""

from yandex_client import OutputMode, generate

TICKET = (
    "С карты дважды списали оплату за сентябрь. "
    "Верните, пожалуйста, лишний платеж как можно быстрее."
)


def main() -> None:
    """Запросить и напечатать неструктурированный ответ модели."""
    result = generate(TICKET, OutputMode.TEXT)
    print(result)


if __name__ == "__main__":
    main()
