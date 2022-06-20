import unittest

from app.perks.todo_perk import TodoPerk


class TestTodoPerk(unittest.TestCase):

    def test_todo(self) -> None:

        todo_perk = TodoPerk()
        todo_perk.create_todo('светлые люди')

