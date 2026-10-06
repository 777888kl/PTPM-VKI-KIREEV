"""Юнит-тесты модуля расчета доставки."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.delivery_service import calculate_delivery_cost


def expected_cost(weight: float, distance: int, package_type: str, is_express: bool = False) -> int:
    total = 200 + distance * 5
    if weight > 5.0 and weight < 20.0:
        total *= 1.2
    elif weight >= 20.0:
        total *= 1.5
    if package_type == "хрупкий":
        total += 300
    elif package_type == "опасный":
        total += 1000
    if is_express:
        total *= 1.5
    return int(total)


def expected_cost(weight: float, distance: int, package_type: str, is_express: bool = False) -> int:
    total = 200 + distance * 5
    if weight > 5.0 and weight < 20.0:
        total *= 1.2
    elif weight >= 20.0:
        total *= 1.5
    if package_type == "хрупкий":
        total += 300
    elif package_type == "опасный":
        total += 1000
    if is_express:
        total *= 1.5
    return int(total)


class TestDeliveryValidation(unittest.TestCase):
    """Границы веса, дистанции и типа посылки."""

    def test_rejects_weight_below_minimum(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_rejects_weight_above_maximum(self):
        cost, date = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_rejects_distance_below_minimum(self):
        cost, date = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_rejects_distance_above_maximum(self):
        cost, date = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_rejects_unknown_package_type(self):
        cost, date = calculate_delivery_cost(1.0, 100, "габаритный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_accepts_boundary_minimum_weight_and_distance(self):
        cost, date = calculate_delivery_cost(0.1, 1, "обычный")
        self.assertNotEqual(cost, -1)
        self.assertNotEqual(date, "0000-00-00")

    def test_accepts_boundary_maximum_weight_and_distance(self):
        cost, date = calculate_delivery_cost(50.0, 5000, "обычный")
        self.assertNotEqual(cost, -1)
        self.assertNotEqual(date, "0000-00-00")


class TestDeliveryPricing(unittest.TestCase):
    """Тарифы: база, вес, тип посылки."""

    def test_calculates_base_cost_for_light_ordinary_package(self):
        # 200 + 100*5 = 700
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_applies_mid_weight_coefficient_for_weight_between_5_and_20(self):
        # (200 + 100*5) * 1.2 = 840
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_applies_heavy_weight_coefficient_for_weight_20_and_above(self):
        # (200 + 100*5) * 1.5 = 1050
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_does_not_apply_weight_coefficient_when_weight_equals_5(self):
        # граница: weight == 5.0 не попадает в (5; 20)
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_adds_surcharge_for_fragile_package(self):
        # 700 + 300 = 1000
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_adds_surcharge_for_dangerous_package(self):
        # 700 + 1000 = 1700
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)

    def test_combines_heavy_weight_and_dangerous_surcharge(self):
        # (200+500)*1.5 + 1000 = 2050
        cost, _ = calculate_delivery_cost(25.0, 100, "опасный")
        self.assertEqual(cost, 2050)


class TestDeliveryExpressAndDate(unittest.TestCase):
    """Экспресс-доставка и расчёт даты."""

    def test_express_delivery_increases_total_cost(self):
        ordinary, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=False)
        express, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertEqual(express, expected_cost(1.0, 100, "обычный", True))
        self.assertGreater(express, ordinary)

    def test_express_cost_matches_restored_business_formula(self):
        # 700 * 1.5 = 1050
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertEqual(cost, 1050)

    def test_ordinary_delivery_date_for_short_distance(self):
        # distance=100 -> days = max(1, 0) = 1 -> 2026-09-04
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_ordinary_delivery_date_for_1000_km(self):
        # days = max(1, 1000//500) = 2 -> 2026-09-05
        _, date = calculate_delivery_cost(1.0, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_express_delivery_keeps_at_least_one_day(self):
        # экспресс не должен давать 0 дней доставки
        _, date = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")

    def test_express_halves_days_but_not_below_one_for_longer_route(self):
        # days=2, express -> max(1, 1) = 1 -> 2026-09-04
        _, date = calculate_delivery_cost(1.0, 1000, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")

    def test_delivery_date_has_iso_format(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")

    def test_default_is_express_false_matches_ordinary_cost(self):
        with_default, _ = calculate_delivery_cost(1.0, 100, "обычный")
        explicit, _ = calculate_delivery_cost(1.0, 100, "обычный", False)
        self.assertEqual(with_default, explicit)
        self.assertEqual(with_default, 700)


if __name__ == "__main__":
    unittest.main()
