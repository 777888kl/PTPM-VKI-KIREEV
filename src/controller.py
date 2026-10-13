"""
Класс-контроллер: сквозная бизнес-логика ЛР3.
"""

from __future__ import annotations

from src.calculator import TriangleCalculator
from src.database import TriangleDatabase
from src.notifier import AbstractNotifier
from src.user_interface import AbstractUserInterface


class TriangleController:
    """
    Сценарий:
    1) запросить стороны у пользователя;
    2) если записи в БД нет — посчитать и сохранить;
       если есть — взять результат из БД;
    3) отправить строку-результат внешней зависимости;
    4) вернуть результат.
    """

    def __init__(
        self,
        user_interface: AbstractUserInterface,
        calculator: TriangleCalculator,
        database: TriangleDatabase,
        notifier: AbstractNotifier,
    ) -> None:
        self._ui = user_interface
        self._calculator = calculator
        self._db = database
        self._notifier = notifier

    def run(self) -> str:
        side_a, side_b, side_c = self._ui.get_sides()

        cached = self._db.get(side_a, side_b, side_c)
        if cached is None:
            triangle_type, error_message, _coords = self._calculator.compute(
                side_a, side_b, side_c
            )
            self._db.add(side_a, side_b, side_c, triangle_type, error_message)
            source = "computed"
        else:
            triangle_type = cached.triangle_type
            error_message = cached.error_message
            source = "database"

        if error_message:
            result = (
                f"source={source}; type={triangle_type!r}; "
                f"error={error_message!r}; sides=({side_a}, {side_b}, {side_c})"
            )
        else:
            result = (
                f"source={source}; type={triangle_type!r}; "
                f"sides=({side_a}, {side_b}, {side_c})"
            )

        self._notifier.send(result)
        return result
