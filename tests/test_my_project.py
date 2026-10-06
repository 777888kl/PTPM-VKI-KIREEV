"""Юнит-тесты для проекта ЛР1 (вычисление вида треугольника). Минимум 20 тестов."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Чтобы unittest discover находил модуль src.my_project
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.my_project import compute_triangle


class TestTriangleClassification(unittest.TestCase):
    """Проверки определения вида треугольника."""

    def test_equilateral_triangle_when_all_sides_equal(self):
        triangle_type, _ = compute_triangle("5", "5", "5")
        self.assertEqual(triangle_type, "равносторонний")

    def test_isosceles_triangle_when_two_sides_equal(self):
        triangle_type, _ = compute_triangle("5", "5", "6")
        self.assertEqual(triangle_type, "равнобедренный")

    def test_isosceles_triangle_when_first_and_third_sides_equal(self):
        triangle_type, _ = compute_triangle("7", "5", "7")
        self.assertEqual(triangle_type, "равнобедренный")

    def test_isosceles_triangle_when_second_and_third_sides_equal(self):
        triangle_type, _ = compute_triangle("4", "8", "8")
        self.assertEqual(triangle_type, "равнобедренный")

    def test_scalene_triangle_for_classic_right_triangle(self):
        triangle_type, _ = compute_triangle("3", "4", "5")
        self.assertEqual(triangle_type, "разносторонний")

    def test_equilateral_triangle_with_float_sides(self):
        triangle_type, _ = compute_triangle("3.5", "3.5", "3.5")
        self.assertEqual(triangle_type, "равносторонний")

    def test_scalene_triangle_with_unequal_float_sides(self):
        triangle_type, _ = compute_triangle("2.5", "3.5", "4.5")
        self.assertEqual(triangle_type, "разносторонний")


class TestTriangleInvalidInput(unittest.TestCase):
    """Проверки некорректных и граничных входных данных."""

    def test_not_a_triangle_when_sides_violate_inequality(self):
        triangle_type, coords = compute_triangle("1", "2", "3")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_not_a_triangle_when_one_side_is_zero(self):
        triangle_type, coords = compute_triangle("0", "5", "5")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_not_a_triangle_when_side_is_negative(self):
        triangle_type, coords = compute_triangle("-1", "4", "5")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_empty_type_when_sides_are_non_numeric(self):
        triangle_type, coords = compute_triangle("a", "b", "c")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_empty_type_when_sides_are_empty_strings(self):
        triangle_type, coords = compute_triangle("", "", "")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_empty_type_when_one_side_is_mixed_text(self):
        triangle_type, coords = compute_triangle("3", "x", "5")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_not_a_triangle_for_degenerate_boundary_case(self):
        # 1 + 1 == 2 — вырожденный «треугольник»
        triangle_type, coords = compute_triangle("1", "1", "2")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_not_a_triangle_when_value_is_infinity(self):
        triangle_type, coords = compute_triangle("inf", "5", "5")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_not_a_triangle_when_value_is_nan(self):
        triangle_type, coords = compute_triangle("nan", "5", "5")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])


class TestTriangleCoordinates(unittest.TestCase):
    """Проверки координат вершин и формата ответа."""

    def test_returns_exactly_three_coordinate_points(self):
        _, coords = compute_triangle("3", "4", "5")
        self.assertEqual(len(coords), 3)

    def test_coordinates_are_integer_pairs(self):
        _, coords = compute_triangle("5", "5", "5")
        for point in coords:
            self.assertIsInstance(point, tuple)
            self.assertEqual(len(point), 2)
            self.assertIsInstance(point[0], int)
            self.assertIsInstance(point[1], int)

    def test_valid_triangle_coordinates_stay_inside_100x100_field(self):
        _, coords = compute_triangle("5", "5", "5")
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_scalene_triangle_coordinates_stay_inside_field(self):
        _, coords = compute_triangle("3", "4", "5")
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_result_is_tuple_of_type_and_coords(self):
        result = compute_triangle("6", "6", "6")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], list)

    def test_parses_sides_with_surrounding_whitespace(self):
        triangle_type, coords = compute_triangle("  5  ", "\t5", "5\n")
        self.assertEqual(triangle_type, "равносторонний")
        self.assertEqual(len(coords), 3)

    def test_accepts_scientific_notation_for_valid_triangle(self):
        triangle_type, _ = compute_triangle("5e0", "5e0", "5e0")
        self.assertEqual(triangle_type, "равносторонний")

    def test_large_sides_still_fit_into_drawing_field(self):
        _, coords = compute_triangle("300", "400", "500")
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_very_small_valid_triangle_has_non_error_coordinates(self):
        triangle_type, coords = compute_triangle("0.2", "0.2", "0.2")
        self.assertEqual(triangle_type, "равносторонний")
        self.assertNotEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])
        self.assertNotEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])


if __name__ == "__main__":
    unittest.main()
