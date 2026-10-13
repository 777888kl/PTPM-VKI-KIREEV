"""
Точка входа Лабораторной работы №3.
Запуск: python main.py
"""

from __future__ import annotations

from src.calculator import TriangleCalculator
from src.controller import TriangleController
from src.database import TriangleDatabase
from src.notifier import EmailNotifier
from src.user_interface import ConsoleUserInterface


def main() -> None:
    db = TriangleDatabase("triangles.db")
    controller = TriangleController(
        user_interface=ConsoleUserInterface(),
        calculator=TriangleCalculator(),
        database=db,
        notifier=EmailNotifier(),
    )

    try:
        result = controller.run()
        print("Результат:", result)
    finally:
        db.close()


if __name__ == "__main__":
    main()
