import unittest
from src.database import DatabaseRepository

class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.repository = DatabaseRepository(":memory:")

    def test_add(self):
        self.repository.add(1, "uuid", "user1", "comment1")
        res = self.repository.get_by_id(1)
        self.assertIsNotNone(res)

    def test_delete(self):
        self.repository.add(1, "uuid", "user1", "comment1")
        self.repository.delete(1)
        res = self.repository.get_by_id(1)
        self.assertIsNone(res)

    def test_get_by_id(self):
        self.repository.add(1, "uuid", "user1", "comment1")
        res = self.repository.get_by_id(1)
        self.assertIsNotNone(res)
        self.assertEqual(res[0], "uuid")
        self.assertEqual(res[1], "user1")
        self.assertEqual(res[2], "comment1")

    def test_get_by_name(self):
        self.repository.add(1, "uuid", "user1", "comment1")
        res = self.repository.get_by_name("user1")
        self.assertIsNotNone(res)
        self.assertEqual(res[0], 1)
        self.assertEqual(res[1], "uuid")
        self.assertEqual(res[2], "comment1")

    def test_update(self):
        self.repository.add(1, "uuid", "user1", "comment1")
        self.repository.update(1, "world")
        res = self.repository.get_by_id(1)
        self.assertEqual(res[2], "world")

    def tearDown(self):
        self.repository.close()

if __name__ == '__main__':
    unittest.main()