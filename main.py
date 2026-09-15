"""
Лабораторная работа №1 — Вариант 1.
Вычисление вида треугольника и координат его вершин.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from core.triangle import compute_triangle


def setup_logging() -> None:
    logs_dir = Path(__file__).resolve().parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logs_dir / "file_txt.log", encoding="utf-8"),
        ],
    )
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")


def main() -> None:
    setup_logging()

    try:
        print("Введите длины сторон треугольника (вещественные положительные числа).")
        side_a = input("Сторона A: ").strip()
        side_b = input("Сторона B: ").strip()
        side_c = input("Сторона C: ").strip()

        logging.info(
            "Успешный приём запроса: a=%r b=%r c=%r",
            side_a,
            side_b,
            side_c,
        )

        triangle_type, coords = compute_triangle(side_a, side_b, side_c)

        print(f"Тип треугольника: {triangle_type!r}")
        print(f"Координаты вершин: {coords}")

        if triangle_type == "" or triangle_type == "не треугольник":
            logging.error(
                "Неуспешный запрос: a=%r b=%r c=%r | type=%r coords=%s",
                side_a,
                side_b,
                side_c,
                triangle_type,
                coords,
            )
        else:
            logging.info(
                "Успешный запрос: a=%r b=%r c=%r | type=%s coords=%s",
                side_a,
                side_b,
                side_c,
                triangle_type,
                coords,
            )

    except Exception:
        logging.error("Что-то пошло не так при обработке запроса...")
        logging.exception("Заход в блок обработки исключения:")
        print("Произошла внутренняя ошибка. Подробности записаны в лог.")
        sys.exit(1)


if __name__ == "__main__":
    main()
