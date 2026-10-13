"""
Класс сторонней зависимости.
Имитация отправки результата на внешний сервер (например, email).
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractNotifier(ABC):
    """Интерфейс отправки данных во внешнюю систему."""

    @abstractmethod
    def send(self, message: str) -> bool:
        """Отправить строку-результат. True — успешная имитация отправки."""


class EmailNotifier(AbstractNotifier):
    """
    Имитация email-сервера.
    Реальной сети нет — только сохраняем последнее сообщение.
    """

    def __init__(self) -> None:
        self.last_message: str | None = None
        self.send_count: int = 0

    def send(self, message: str) -> bool:
        # имитация передачи данных стороннему процессу
        self.last_message = message
        self.send_count += 1
        print(f"[EmailNotifier] отправлено на внешний сервер: {message}")
        return True
