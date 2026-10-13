"""
Тесты изоляции модулей через заглушки (unittest.mock).
Проверяем UI (input) и внешний notifier отдельно от бизнес-логики треугольника.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from src.notifier import EmailNotifier
from src.user_interface import ConsoleUserInterface


class TestStubsAndMocks(unittest.TestCase):
    @patch("builtins.input", side_effect=["3", "4", "5"])
    def test_console_ui_reads_three_sides_via_input_stub(self, mock_input: MagicMock) -> None:
        ui = ConsoleUserInterface()
        sides = ui.get_sides()

        self.assertEqual(sides, ("3", "4", "5"))
        self.assertEqual(mock_input.call_count, 3)

    def test_email_notifier_stores_sent_message(self) -> None:
        notifier = EmailNotifier()
        ok = notifier.send("hello-server")

        self.assertTrue(ok)
        self.assertEqual(notifier.last_message, "hello-server")
        self.assertEqual(notifier.send_count, 1)


if __name__ == "__main__":
    unittest.main()
