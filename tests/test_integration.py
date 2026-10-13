"""
Интеграционные тесты контроллера.
Связываем UI + Calculator + DB + Notifier.
Ввод пользователя и внешний сервер подменяем заглушками.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from src.calculator import TriangleCalculator
from src.controller import TriangleController
from src.database import TriangleDatabase
from src.notifier import AbstractNotifier
from src.user_interface import AbstractUserInterface


class FakeUserInterface(AbstractUserInterface):
    """Заглушка пользовательского ввода."""

    def __init__(self, sides: tuple[str, str, str]) -> None:
        self._sides = sides

    def get_sides(self) -> tuple[str, str, str]:
        return self._sides


class FakeNotifier(AbstractNotifier):
    """Заглушка внешней зависимости (email-сервер)."""

    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> bool:
        self.messages.append(message)
        return True


class TestTriangleControllerIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.db = TriangleDatabase(":memory:")
        self.notifier = FakeNotifier()
        self.calculator = TriangleCalculator()

    def tearDown(self) -> None:
        self.db.close()

    def _make_controller(self, sides: tuple[str, str, str]) -> TriangleController:
        return TriangleController(
            user_interface=FakeUserInterface(sides),
            calculator=self.calculator,
            database=self.db,
            notifier=self.notifier,
        )

    def test_integration_computes_and_saves_when_db_empty(self) -> None:
        """Интеграция: нет записи в БД → считаем → кладем в БД → шлем наружу."""
        controller = self._make_controller(("3", "4", "5"))
        result = controller.run()

        self.assertIn("source=computed", result)
        self.assertIn("разносторонний", result)

        cached = self.db.get("3", "4", "5")
        self.assertIsNotNone(cached)
        assert cached is not None
        self.assertEqual(cached.triangle_type, "разносторонний")
        self.assertEqual(len(self.notifier.messages), 1)
        self.assertEqual(self.notifier.messages[0], result)

    def test_integration_reads_from_database_on_second_call(self) -> None:
        """Интеграция: повторный запрос берет результат из БД, без пересчета."""
        sides = ("5", "5", "5")
        first = self._make_controller(sides).run()
        self.assertIn("source=computed", first)

        # подмена калькулятора: если контроллер снова пойдет в compute — упадём
        spy_calculator = MagicMock(wraps=self.calculator)
        second_controller = TriangleController(
            user_interface=FakeUserInterface(sides),
            calculator=spy_calculator,
            database=self.db,
            notifier=self.notifier,
        )
        second = second_controller.run()

        self.assertIn("source=database", second)
        self.assertIn("равносторонний", second)
        spy_calculator.compute.assert_not_called()
        self.assertEqual(len(self.notifier.messages), 2)

    def test_integration_invalid_input_saves_error_and_notifies(self) -> None:
        """Интеграция: нечисловой ввод → ошибка в БД + отправка на «сервер»."""
        controller = self._make_controller(("a", "b", "c"))
        result = controller.run()

        self.assertIn("source=computed", result)
        self.assertIn("нечисловые данные", result)

        cached = self.db.get("a", "b", "c")
        self.assertIsNotNone(cached)
        assert cached is not None
        self.assertEqual(cached.triangle_type, "")
        self.assertEqual(cached.error_message, "нечисловые данные")
        self.assertTrue(self.notifier.messages)

    def test_integration_non_triangle_sides_flow(self) -> None:
        """Интеграция: числа есть, но треугольник не образуется."""
        controller = self._make_controller(("1", "2", "3"))
        result = controller.run()

        self.assertIn("не треугольник", result)
        self.assertIn("некорректные стороны", result)
        cached = self.db.get("1", "2", "3")
        self.assertIsNotNone(cached)
        assert cached is not None
        self.assertEqual(cached.triangle_type, "не треугольник")


if __name__ == "__main__":
    unittest.main()
