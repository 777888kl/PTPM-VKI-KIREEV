import sqlite3
from typing import Any, Dict, List, Optional


class DatabaseRepository:
    """Репозиторий для управления комментариями форума в базе данных SQLite."""

    MAX_NAME_LENGTH = 256
    MAX_MESSAGE_LENGTH = 8096

    def __init__(self, db_path: str = ":memory:") -> None:
        """Инициализация подключения и создание таблицы, если она отсутствует."""
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Создает и возвращает подключение с row_factory для отдачи словарей."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Создает таблицу comments с заданными ограничениями схемы."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        );
        """
        with self._get_connection() as conn:
            conn.execute(create_table_sql)

    def _validate_data(
        self,
        comment_id: Optional[int] = None,
        username: Optional[str] = None,
        message: Optional[str] = None,
    ) -> None:
        """Валидация типов данных и длины строк."""
        if comment_id is not None:
            if not isinstance(comment_id, int) or isinstance(comment_id, bool):
                raise TypeError("comment_id должен быть целым числом.")

        if username is not None:
            if not isinstance(username, str):
                raise TypeError("username должен быть строкой.")
            if len(username.strip()) == 0:
                raise ValueError("username не может быть пустым.")
            if len(username) > self.MAX_NAME_LENGTH:
                raise ValueError(
                    f"username превышает допустимую длину ({self.MAX_NAME_LENGTH} символов)."
                )

        if message is not None:
            if not isinstance(message, str):
                raise TypeError("message должен быть строкой.")
            if len(message.strip()) == 0:
                raise ValueError("message не может быть пустым.")
            if len(message) > self.MAX_MESSAGE_LENGTH:
                raise ValueError(
                    f"message превышает допустимую длину ({self.MAX_MESSAGE_LENGTH} символов)."
                )

    def add(self, comment_id: int, username: str, message: str) -> bool:
        """
        Добавляет новую запись в БД.
        Возвращает True при успешной вставке.
        Выбрасывает ValueError / TypeError при некорректных данных
        или sqlite3.IntegrityError при дублировании ID.
        """
        self._validate_data(comment_id=comment_id, username=username, message=message)

        sql = "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)"
        with self._get_connection() as conn:
            conn.execute(sql, (comment_id, username, message))
        return True

    def get_by_id(self, comment_id: int) -> Optional[Dict[str, Any]]:
        """Возвращает запись по comment_id в виде словаря или None."""
        self._validate_data(comment_id=comment_id)

        sql = "SELECT id, name, message FROM comments WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.execute(sql, (comment_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_by_name(self, username: str) -> List[Dict[str, Any]]:
        """Возвращает список всех комментариев пользователя."""
        if not isinstance(username, str):
            raise TypeError("username должен быть строкой.")

        sql = "SELECT id, name, message FROM comments WHERE name = ? ORDER BY id ASC"
        with self._get_connection() as conn:
            cursor = conn.execute(sql, (username,))
            return [dict(row) for row in cursor.fetchall()]

    def update(self, comment_id: int, new_message: str) -> bool:
        """
        Обновляет текст комментария.
        Выбрасывает KeyError, если запись с указанным ID не найдена.
        """
        self._validate_data(comment_id=comment_id, message=new_message)

        sql = "UPDATE comments SET message = ? WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.execute(sql, (new_message, comment_id))
            if cursor.rowcount == 0:
                raise KeyError(f"Запись с comment_id={comment_id} не найдена.")
        return True

    def delete(self, comment_id: int) -> bool:
        """
        Удаляет запись по ID.
        Возвращает True, если строка была удалена, иначе False.
        """
        self._validate_data(comment_id=comment_id)

        sql = "DELETE FROM comments WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.execute(sql, (comment_id,))
            return cursor.rowcount > 0