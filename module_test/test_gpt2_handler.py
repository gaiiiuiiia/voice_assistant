import unittest

from app.core.text_generators.gpt2.gpt2_handler import GPT2Handler
import app.config as config


class TestGpt2Handler(unittest.TestCase):

    def setUp(self) -> None:
        self._gpt2 = GPT2Handler(config.GPT2_SERVER_URL)

    def test_generate(self) -> None:
        self._gpt2.generate('привет')
