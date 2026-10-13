"""
Класс вычислений / валидации.
Метод из Лабораторной работы №1 (определение вида треугольника).
"""

from __future__ import annotations

import math
from typing import List, Tuple

Point = Tuple[int, int]
Coords = List[Point]

FIELD_SIZE = 100
EPS = 1e-9
INVALID_NON_NUMERIC: Coords = [(-2, -2), (-2, -2), (-2, -2)]
INVALID_NUMERIC: Coords = [(-1, -1), (-1, -1), (-1, -1)]


class TriangleCalculator:
    """Вычисление типа треугольника по трем сторонам."""

    def compute(self, side_a: str, side_b: str, side_c: str) -> tuple[str, str, Coords]:
        """
        Возвращает (тип_треугольника, сообщение_об_ошибке, координаты).

        Ошибки:
        - нечисловые данные -> ("", "нечисловые данные", [(-2,-2)]*3)
        - не треугольник    -> ("не треугольник", "некорректные стороны", [(-1,-1)]*3)
        """
        parsed = self._parse_sides(side_a, side_b, side_c)
        if parsed is None:
            return "", "нечисловые данные", list(INVALID_NON_NUMERIC)

        a, b, c = parsed
        if not self._is_valid_triangle(a, b, c):
            return "не треугольник", "некорректные стороны", list(INVALID_NUMERIC)

        triangle_type = self._classify(a, b, c)
        coords = self._fit_to_field(self._raw_vertices(a, b, c))
        return triangle_type, "", coords

    @staticmethod
    def _parse_sides(side_a: str, side_b: str, side_c: str) -> tuple[float, float, float] | None:
        try:
            a = float(str(side_a).strip())
            b = float(str(side_b).strip())
            c = float(str(side_c).strip())
        except (TypeError, ValueError, AttributeError):
            return None
        return a, b, c

    @staticmethod
    def _is_valid_triangle(a: float, b: float, c: float) -> bool:
        if a <= 0 or b <= 0 or c <= 0:
            return False
        if math.isinf(a) or math.isinf(b) or math.isinf(c):
            return False
        if math.isnan(a) or math.isnan(b) or math.isnan(c):
            return False
        return a + b > c + EPS and a + c > b + EPS and b + c > a + EPS

    @staticmethod
    def _nearly_equal(x: float, y: float) -> bool:
        return abs(x - y) < EPS

    def _classify(self, a: float, b: float, c: float) -> str:
        ab = self._nearly_equal(a, b)
        bc = self._nearly_equal(b, c)
        ac = self._nearly_equal(a, c)
        if ab and bc:
            return "равносторонний"
        if ab or bc or ac:
            return "равнобедренный"
        return "разносторонний"

    @staticmethod
    def _raw_vertices(a: float, b: float, c: float) -> list[tuple[float, float]]:
        x = (b * b + a * a - c * c) / (2.0 * a)
        y_sq = b * b - x * x
        if y_sq < 0 and abs(y_sq) < EPS:
            y_sq = 0.0
        y = math.sqrt(max(y_sq, 0.0))
        return [(0.0, 0.0), (a, 0.0), (x, y)]

    @staticmethod
    def _fit_to_field(points: list[tuple[float, float]]) -> Coords:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width = max_x - min_x
        height = max_y - min_y

        if width < EPS and height < EPS:
            cx = FIELD_SIZE // 2
            return [(cx, cx), (cx, cx), (cx, cx)]

        scale = FIELD_SIZE / max(width, height, EPS)
        result: Coords = []
        for x, y in points:
            ix = int(round((x - min_x) * scale))
            iy = int(round((y - min_y) * scale))
            ix = max(0, min(FIELD_SIZE, ix))
            iy = max(0, min(FIELD_SIZE, iy))
            result.append((ix, iy))
        return result
