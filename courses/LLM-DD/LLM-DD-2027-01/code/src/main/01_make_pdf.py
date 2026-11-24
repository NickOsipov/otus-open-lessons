"""Module: 01_make_pdf
Description: Собрать учебный PDF магазина Орбита: 4 страницы с текстом и колонтитулами плюс страница-скан.
"""

import pymupdf

from config.variables import DATA_DIR, PDF_PATH

PAGE_WIDTH = 595
PAGE_HEIGHT = 842
SCAN_DPI = 110
HEADER_TEXT = "Орбита - руководство покупателя"
FOOTER_TEMPLATE = "Страница {number} из {total} - редакция 2026"
TEXT_STYLE = "font-family: sans-serif; font-size: 12px; line-height: 1.4;"
MARGIN_STYLE = "font-family: sans-serif; font-size: 9px; color: #777777;"

PAGES = [
    (
        "Доставка",
        "Курьер Орбиты привозит заказ за 1-3 рабочих дня в пределах города. "
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
        "Сдать устройство в ремонт можно в сервисный центр Орбиты на улице Лесной, дом 12, "
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
    "Клиент передает устройство в ремонт. Внешний вид, комплектность и "
    "серийный номер проверены. Срок ремонта не более 21 дня.",
)


def draw_page(page: pymupdf.Page, title: str, body: str, number: int, total: int) -> None:
    """Нарисовать на странице колонтитул, заголовок, текст и подвал с номером."""
    page.insert_htmlbox(
        pymupdf.Rect(40, 18, 555, 42),
        f"<p style='{MARGIN_STYLE}'>{HEADER_TEXT}</p>",
    )
    page.insert_htmlbox(
        pymupdf.Rect(60, 70, 535, 780),
        f"<div style='{TEXT_STYLE}'><h2>{title}</h2><p>{body}</p></div>",
    )
    page.insert_htmlbox(
        pymupdf.Rect(40, 805, 555, 830),
        f"<p style='{MARGIN_STYLE}'>{FOOTER_TEMPLATE.format(number=number, total=total)}</p>",
    )


def add_scan_page(doc: pymupdf.Document, number: int, total: int) -> None:
    """Добавить страницу без текстового слоя: только картинка отрисованной страницы."""
    draft = pymupdf.open()
    draft_page = draft.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    draw_page(draft_page, SCAN_PAGE[0], SCAN_PAGE[1], number, total)
    pixmap = draft_page.get_pixmap(dpi=SCAN_DPI)
    draft.close()

    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    page.insert_image(page.rect, pixmap=pixmap)


def build_pdf() -> None:
    """Собрать PDF из текстовых страниц и одной страницы-скана."""
    DATA_DIR.mkdir(exist_ok=True)
    total = len(PAGES) + 1
    doc = pymupdf.open()
    doc.set_metadata({"title": "Руководство покупателя Орбита", "author": "Орбита"})

    for number, (title, body) in enumerate(PAGES, start=1):
        page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        draw_page(page, title, body, number, total)
    add_scan_page(doc, total, total)

    doc.save(PDF_PATH)
    doc.close()
    print(f"saved {PDF_PATH.name}: {total} pages")


if __name__ == "__main__":
    build_pdf()
