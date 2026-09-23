"""Module: pdf_to_markdown
Description: Извлекает содержимое PDF-программ и сохраняет его в Markdown.
"""

import argparse
import sys
from pathlib import Path

import pymupdf4llm


def parse_args() -> argparse.Namespace:
    """Разобрать аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Преобразовать PDF-файл или каталог с PDF-файлами в Markdown.",
    )
    parser.add_argument(
        "-s",
        "--source",
        type=Path,
        help="Путь к PDF-файлу или каталогу с PDF-файлами.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help=(
            "Путь к итоговому .md для одного PDF или каталог для нескольких PDF. "
            "По умолчанию Markdown сохраняется рядом с исходным файлом."
        ),
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Искать PDF во вложенных каталогах.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Перезаписывать существующие Markdown-файлы.",
    )
    return parser.parse_args()


def find_pdf_files(source: Path, recursive: bool) -> list[Path]:
    """Найти PDF-файлы в указанном файле или каталоге."""
    if not source.exists():
        raise FileNotFoundError(f"Путь не найден: {source}")

    if source.is_file():
        if source.suffix.lower() != ".pdf":
            raise ValueError(f"Ожидался PDF-файл: {source}")
        return [source]

    pattern = "**/*" if recursive else "*"
    return sorted(
        path for path in source.glob(pattern) if path.is_file() and path.suffix.lower() == ".pdf"
    )


def get_output_path(
    pdf_path: Path,
    source: Path,
    output: Path | None,
    multiple_files: bool,
) -> Path:
    """Определить путь итогового Markdown-файла."""
    if output is None:
        return pdf_path.with_suffix(".md")

    if source.is_file() and not multiple_files and output.suffix.lower() == ".md":
        return output

    relative_path = pdf_path.relative_to(source) if source.is_dir() else Path(pdf_path.name)
    return (output / relative_path).with_suffix(".md")


def convert_pdf(pdf_path: Path, output_path: Path, overwrite: bool) -> None:
    """Преобразовать один PDF-файл в Markdown и записать результат."""
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Файл уже существует: {output_path}. Используйте --overwrite для перезаписи."
        )

    markdown = pymupdf4llm.to_markdown(str(pdf_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    """Запустить преобразование PDF-файлов и вернуть код завершения."""
    args = parse_args()

    try:
        pdf_files = find_pdf_files(args.source, args.recursive)
    except (FileNotFoundError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 2

    if not pdf_files:
        print(f"PDF-файлы не найдены: {args.source}", file=sys.stderr)
        return 1

    failed = 0
    for pdf_path in pdf_files:
        output_path = get_output_path(
            pdf_path=pdf_path,
            source=args.source,
            output=args.output,
            multiple_files=len(pdf_files) > 1,
        )
        try:
            convert_pdf(pdf_path, output_path, args.overwrite)
            print(f"Готово: {pdf_path} -> {output_path}")
        except (FileExistsError, OSError, RuntimeError, ValueError) as error:
            failed += 1
            print(f"Ошибка при обработке {pdf_path}: {error}", file=sys.stderr)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
