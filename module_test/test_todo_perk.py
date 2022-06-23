import unittest

from app.perks.todo_perk import TodoPerk


class TestTodoPerk(unittest.TestCase):

    def setUp(self) -> None:
        self._todo_perk = TodoPerk()

    def test_create_todo(self) -> None:
        self._todo_perk.create_todo(query='светлые люди')

    def test_read_todo(self) -> None:
        self._todo_perk.read_todo()

