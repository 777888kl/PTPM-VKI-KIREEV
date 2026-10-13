"""
Класс работы с базой данных SQLite.
Запись треугольника: длина1, длина2, длина3, тип, сообщение_об_ошибке.
Идентификация по трем длинам сторон.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional


@dataclass
class TriangleRecord:
    side1: str
    side2: str
    side3: str
    triangle_type: str
    error_message: str


class TriangleDatabase:
    """CRUD для результатов вычисления треугольника."""

    def __init__(self, db_path: str = ":memory:") -> None:
        # :memory: — удобно для тестов; можно передать путь к файлу
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS triangles (
                side1 TEXT NOT NULL,
                side2 TEXT NOT NULL,
                side3 TEXT NOT NULL,
                triangle_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                PRIMARY KEY (side1, side2, side3)
            )
            """
        )
        self._connection.commit()

    def add(
        self,
        side1: str,
        side2: str,
        side3: str,
        triangle_type: str,
        error_message: str = "",
    ) -> None:
        """Добавление записи (или замена, если уже есть такой ключ)."""
        self._connection.execute(
            """
            INSERT OR REPLACE INTO triangles
            (side1, side2, side3, triangle_type, error_message)
            VALUES (?, ?, ?, ?, ?)
            """,
            (side1, side2, side3, triangle_type, error_message),
        )
        self._connection.commit()

    def get(self, side1: str, side2: str, side3: str) -> Optional[TriangleRecord]:
        """Получение записи по трем сторонам. None — если нет в БД."""
        cursor = self._connection.execute(
            """
            SELECT side1, side2, side3, triangle_type, error_message
            FROM triangles
            WHERE side1 = ? AND side2 = ? AND side3 = ?
            """,
            (side1, side2, side3),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return TriangleRecord(
            side1=row["side1"],
            side2=row["side2"],
            side3=row["side3"],
            triangle_type=row["triangle_type"],
            error_message=row["error_message"],
        )

    def delete(self, side1: str, side2: str, side3: str) -> bool:
        """Удаление записи. True — если что-то удалили."""
        cursor = self._connection.execute(
            """
            DELETE FROM triangles
            WHERE side1 = ? AND side2 = ? AND side3 = ?
            """,
            (side1, side2, side3),
        )
        self._connection.commit()
        return cursor.rowcount > 0

    def close(self) -> None:
        self._connection.close()
