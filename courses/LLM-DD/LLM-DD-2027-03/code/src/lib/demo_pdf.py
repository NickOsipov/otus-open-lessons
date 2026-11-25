"""Module: demo_pdf
Description: Текст учебного руководства интернет-магазина и отрисовка страниц, включая страницу-скан без текстового слоя.
"""

import pymupdf

PAGE_WIDTH = 595
PAGE_HEIGHT = 842
SCAN_DPI = 150
HEADER_TEXT = "Интернет-магазин - руководство покупателя"
FOOTER_TEMPLATE = "Страница {number} из {total} - редакция 2026"
TEXT_STYLE = "font-family: sans-serif; font-size: 12px; line-height: 1.4;"
SCAN_STYLE = "font-family: sans-serif; font-size: 16px; line-height: 1.5;"
MARGIN_STYLE = "font-family: sans-serif; font-size: 9px; color: #777777;"

PAGES = [
    (
        "Доставка",
        "Курьер магазина привозит заказ за 1-3 рабочих дня в пределах города. "
        "Доставка в пункт выдачи занимает до 5 рабочих дней. "
        "Заказ хранится в пункте выдачи 7 дней, затем возвращается на склад.",
    ),
    (
        "Возврат товара",
        "Товар надлежащего качества можно вернуть в течение 14 дней. "
        "Заявка оформляется в личном кабинете в разделе Заказы. "
        "Деньги возвращаются на карту, с которой оплачен заказ, за 3-10 дней.",
    ),
    (
        "Гарантия и ремонт",
        "Гарантия на ремонт составляет 6 месяцев с даты выдачи устройства после ремонта. "
        "Сдать устройство в ремонт можно в сервисный центр магазина на улице Лесной, дом 12, "
        "или передать курьеру при оформлении заявки в личном кабинете. "
        "Диагностика бесплатна, если неисправность подпадает под гарантию.",
    ),
    (
        "Уход за устройством",
        "Не заряжайте устройство неоригинальными адаптерами. "
        "Храните его при температуре от 0 до 35 градусов. "
        "Для чистки экрана используйте сухую мягкую ткань без спирта.",
    ),
]

SCAN_PAGE = (
    "Акт приема устройства",
    "Клиент передает устройство в ремонт. Внешний вид и комплектность проверены. "
    "Серийный номер: SN-7781-204. Срок ремонта не более 21 рабочего дня.",
)
TOTAL_PAGES = len(PAGES) + 1
SCAN_KEY_FIELDS = ("SN-7781-204", "21")


def footer_text(number: int) -> str:
    """Вернуть подпись подвала с номером страницы из общего числа страниц."""
    return FOOTER_TEMPLATE.format(number=number, total=TOTAL_PAGES)


def draw_page(page: pymupdf.Page, title: str, body: str, number: int, style: str) -> None:
    """Нарисовать на странице колонтитул, заголовок с текстом и подвал с номером."""
    page.insert_htmlbox(
        pymupdf.Rect(40, 18, 555, 42),
        f"<p style='{MARGIN_STYLE}'>{HEADER_TEXT}</p>",
    )
    page.insert_htmlbox(
        pymupdf.Rect(60, 70, 535, 780),
        f"<div style='{style}'><h2>{title}</h2><p>{body}</p></div>",
    )
    page.insert_htmlbox(
        pymupdf.Rect(40, 805, 555, 830),
        f"<p style='{MARGIN_STYLE}'>{footer_text(number)}</p>",
    )


def scan_source_text() -> str:
    """Вернуть исходный текст страницы-скана: эталон для проверки OCR в демо."""
    title, body = SCAN_PAGE
    return "\n".join([HEADER_TEXT, title, body, footer_text(TOTAL_PAGES)])


def make_scan_image() -> bytes:
    """Нарисовать страницу-скан во временном документе и вернуть ее PNG-картинкой."""
    title, body = SCAN_PAGE
    draft = pymupdf.open()
    draft_page = draft.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    draw_page(draft_page, title, body, TOTAL_PAGES, SCAN_STYLE)
    png = draft_page.get_pixmap(dpi=SCAN_DPI).tobytes("png")
    draft.close()
    return png
