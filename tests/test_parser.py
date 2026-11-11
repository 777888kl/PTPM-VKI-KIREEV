import os
import unittest
from src.database import DatabaseRepository
from src.parser import ForumParser


class TestForumParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Чтение локального HTML-слепка перед запуском тестового набора."""
        fixture_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "forum_mock.html"
        )
        with open(fixture_path, "r", encoding="utf-8") as f:
            cls.fixture_html = f.read()

    def setUp(self) -> None:
        self.parser = ForumParser()
        self.repo = DatabaseRepository(":memory:")

    def test_parse_html_extracts_correct_fields(self) -> None:
        """Проверка корректности извлечения ID, имени и вложенного HTML."""
        items = self.parser.parse_html(self.fixture_html)

        self.assertEqual(len(items), 2)

        first_post = items[0]
        self.assertEqual(first_post["comment_id"], 101)
        self.assertEqual(first_post["name"], "SeniorDev")
        self.assertIn("<b>requests</b>", first_post["message"])

        second_post = items[1]
        self.assertEqual(second_post["comment_id"], 102)
        self.assertEqual(second_post["name"], "JuniorLearner")
        self.assertIn('<a href="#101">@SeniorDev</a>', second_post["message"])

    def test_save_to_db_persists_extracted_entities(self) -> None:
        """Проверка цепочки сохранения распарсенных данных в базу данных."""
        items = self.parser.parse_html(self.fixture_html)
        saved_count = self.parser.save_to_db(items, self.repo)

        self.assertEqual(saved_count, 2)

        db_item = self.repo.get_by_id(101)
        self.assertIsNotNone(db_item)
        self.assertEqual(db_item["name"], "SeniorDev")

    def test_save_to_db_ignores_duplicates_gracefully(self) -> None:
        """Проверка устойчивости save_to_db к повторной записи тех же данных."""
        items = self.parser.parse_html(self.fixture_html)
        self.parser.save_to_db(items, self.repo)

        # Повторная попытка сохранить те же записи не должна ронять программу
        second_run_saved = self.parser.save_to_db(items, self.repo)
        self.assertEqual(second_run_saved, 0)


if __name__ == "__main__":
    unittest.main()
