"""
Класс взаимодействия с пользователем.
Абстрактный базовый класс (интерфейс) + консольная реализация через input().
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractUserInterface(ABC):
    """Интерфейс получения входных данных от пользователя."""

    @abstractmethod
    def get_sides(self) -> tuple[str, str, str]:
        """Вернуть три стороны треугольника как строки."""


class ConsoleUserInterface(AbstractUserInterface):
    """Чтение сторон через консольный input()."""

    def get_sides(self) -> tuple[str, str, str]:
        side_a = input("Введите сторону A: ").strip()
        side_b = input("Введите сторону B: ").strip()
        side_c = input("Введите сторону C: ").strip()
        return side_a, side_b, side_c
