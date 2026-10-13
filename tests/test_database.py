"""Юнит-тесты класса работы с БД (не дублируют проверки ЛР2)."""

from __future__ import annotations

import unittest

from src.database import TriangleDatabase


class TestTriangleDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.db = TriangleDatabase(":memory:")

    def tearDown(self) -> None:
        self.db.close()

    def test_add_and_get_record(self) -> None:
        self.db.add("3", "4", "5", "разносторонний", "")
        record = self.db.get("3", "4", "5")

        self.assertIsNotNone(record)
        assert record is not None
        self.assertEqual(record.triangle_type, "разносторонний")
        self.assertEqual(record.error_message, "")

    def test_get_returns_none_when_missing(self) -> None:
        self.assertIsNone(self.db.get("1", "1", "1"))

    def test_delete_removes_record(self) -> None:
        self.db.add("5", "5", "5", "равносторонний", "")
        deleted = self.db.delete("5", "5", "5")

        self.assertTrue(deleted)
        self.assertIsNone(self.db.get("5", "5", "5"))


if __name__ == "__main__":
    unittest.main()
