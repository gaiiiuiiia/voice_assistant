import unittest

from app.perks.todo_perk import TodoPerk


class TestTodoPerk(unittest.TestCase):

    def setUpClass(self) -> None:
        self._todo_perk = TodoPerk()

    def tearDownClass(self) -> None:
        self._todo_perk.delete_todo()

    def test_create_todo(self) -> None:
        self._todo_perk.create_todo('светлые люди')

    def test_read_todo(self) -> None:
        self.assertEqual(self._todo_perk.read_todo(), 'светлые люди')

