"""Определение вида треугольника и координат вершин в поле 100x100."""

from __future__ import annotations

import logging
import math
from typing import List, Tuple

logger = logging.getLogger(__name__)

Point = Tuple[int, int]
Coords = List[Point]

FIELD_SIZE = 100
EPS = 1e-9

INVALID_NON_NUMERIC: Coords = [(-2, -2), (-2, -2), (-2, -2)]
INVALID_NUMERIC: Coords = [(-1, -1), (-1, -1), (-1, -1)]


def _nearly_equal(x: float, y: float) -> bool:
    return abs(x - y) < EPS


def _parse_sides(side_a: str, side_b: str, side_c: str) -> tuple[float, float, float] | None:
    try:
        a = float(side_a.strip())
        b = float(side_b.strip())
        c = float(side_c.strip())
    except (TypeError, ValueError):
        return None
    return a, b, c


def _is_valid_triangle(a: float, b: float, c: float) -> bool:
    if a <= 0 or b <= 0 or c <= 0:
        return False
    if math.isinf(a) or math.isinf(b) or math.isinf(c):
        return False
    if math.isnan(a) or math.isnan(b) or math.isnan(c):
        return False
    return (
        a + b > c + EPS
        and a + c > b + EPS
        and b + c > a + EPS
    )


def _classify(a: float, b: float, c: float) -> str:
    ab = _nearly_equal(a, b)
    bc = _nearly_equal(b, c)
    ac = _nearly_equal(a, c)
    if ab and bc:
        return "равносторонний"
    if ab or bc or ac:
        return "равнобедренный"
    return "разносторонний"


def _raw_vertices(a: float, b: float, c: float) -> list[tuple[float, float]]:
    """Размещает треугольник: A(0,0), B(a,0), C(x,y)."""
    x = (b * b + a * a - c * c) / (2.0 * a)
    y_sq = b * b - x * x
    if y_sq < 0 and abs(y_sq) < EPS:
        y_sq = 0.0
    y = math.sqrt(max(y_sq, 0.0))
    return [(0.0, 0.0), (a, 0.0), (x, y)]


def _fit_to_field(points: list[tuple[float, float]]) -> Coords:
    """Масштабирует и сдвигает точки в целочисленное поле [0, FIELD_SIZE]."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y

    # Запас 1 px с каждой стороны при ненулевом размере
    usable = FIELD_SIZE
    if width < EPS and height < EPS:
        # вырожденный случай — все в центре
        cx = FIELD_SIZE // 2
        return [(cx, cx), (cx, cx), (cx, cx)]

    scale = usable / max(width, height, EPS)

    result: Coords = []
    for x, y in points:
        nx = (x - min_x) * scale
        ny = (y - min_y) * scale
        ix = int(round(nx))
        iy = int(round(ny))
        ix = max(0, min(FIELD_SIZE, ix))
        iy = max(0, min(FIELD_SIZE, iy))
        result.append((ix, iy))
    return result


def compute_triangle(side_a: str, side_b: str, side_c: str) -> tuple[str, Coords]:
    """
    По трём сторонам возвращает вид треугольника и координаты вершин.

    Нечисловые данные -> ("", [(-2,-2)] * 3)
    Некорректные числа / не треугольник -> ("не треугольник", [(-1,-1)] * 3)
    """
    logger.debug(
        "compute_triangle: вход side_a=%r side_b=%r side_c=%r",
        side_a,
        side_b,
        side_c,
    )

    parsed = _parse_sides(side_a, side_b, side_c)
    if parsed is None:
        logger.warning(
            "Нечисловые входные данные: a=%r b=%r c=%r",
            side_a,
            side_b,
            side_c,
        )
        return "", list(INVALID_NON_NUMERIC)

    a, b, c = parsed
    logger.debug("Распарсенные стороны: a=%s b=%s c=%s", a, b, c)

    if not _is_valid_triangle(a, b, c):
        logger.warning(
            "Некорректные числовые данные / не треугольник: a=%s b=%s c=%s",
            a,
            b,
            c,
        )
        return "не треугольник", list(INVALID_NUMERIC)

    triangle_type = _classify(a, b, c)
    coords = _fit_to_field(_raw_vertices(a, b, c))
    logger.info(
        "Треугольник определён: type=%s coords=%s (стороны a=%s b=%s c=%s)",
        triangle_type,
        coords,
        a,
        b,
        c,
    )
    return triangle_type, coords
