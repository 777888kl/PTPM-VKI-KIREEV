from typing import Any, Dict, List
from bs4 import BeautifulSoup
import requests
from src.database import DatabaseRepository


class ForumParser:
    """Компонент сбора данных со страниц форумов."""

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    def __init__(self, headers: Dict[str, str] = None, timeout: int = 10) -> None:
        self.headers = headers or self.DEFAULT_HEADERS
        self.timeout = timeout

    def fetch_page(self, url: str) -> str:
        """Скачивает HTML-код страницы по URL."""
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def parse_html(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Парсит HTML-разметку и извлекает список комментариев.

        Ожидаемая селекторная модель элементов форума:
          - Контейнер поста: [data-post-id] или class='post' / class='comment'
          - Автор: класс .post-author или .username
          - Тело сообщения: класс .post-message или .comment-body
        """
        soup = BeautifulSoup(html_content, "lxml")
        results: List[Dict[str, Any]] = []

        posts = soup.find_all(
            lambda tag: tag.has_attr("data-post-id")
            or "post" in tag.get("class", [])
            or "comment" in tag.get("class", [])
        )

        for post in posts:
            raw_id = post.get("data-post-id") or post.get("id", "").replace("post-", "")
            if not raw_id or not str(raw_id).isdigit():
                continue

            comment_id = int(raw_id)

            author_tag = post.find(class_=["post-author", "username", "author"])
            author_name = author_tag.get_text(strip=True) if author_tag else "Anonymous"

            content_tag = post.find(class_=["post-message", "comment-body", "message"])
            if content_tag:
                message_html = "".join(str(child) for child in content_tag.contents).strip()
            else:
                message_html = ""

            results.append(
                {
                    "comment_id": comment_id,
                    "name": author_name,
                    "message": message_html,
                }
            )

        return results

    def parse_page(self, url: str) -> List[Dict[str, Any]]:
        """Загружает страницу по URL и возвращает распарсенные данные."""
        html = self.fetch_page(url)
        return self.parse_html(html)

    def save_to_db(
        self, parsed_data: List[Dict[str, Any]], repository: DatabaseRepository
    ) -> int:
        """
        Сохраняет распарсенные сущности в базу данных через DatabaseRepository.
        Возвращает количество успешно вставленных записей.
        """
        saved_count = 0
        for item in parsed_data:
            try:
                repository.add(
                    comment_id=item["comment_id"],
                    username=item["name"],
                    message=item["message"],
                )
                saved_count += 1
            except Exception:
                # Пропускаем дубликаты ID или невалидные строки, продолжая обработку
                continue
        return saved_count