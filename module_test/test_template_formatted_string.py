import unittest

from app.core.template_format_string import TemplateFormatString


class TestTemplateFormattedString(unittest.TestCase):

    def test_compile(self) -> None:
        self.assertEqual(TemplateFormatString('привет %world%!', {'world': 'мир'}).compile(), 'привет мир!')
        self.assertEqual(TemplateFormatString('привет мир!').compile(), 'привет мир!')
        self.assertEqual(TemplateFormatString('').compile(), '')
        self.assertEqual(TemplateFormatString('%world%', {'world': 'мир'}).compile(), 'мир')

    def test_is_template_text(self) -> None:
        self.assertTrue(TemplateFormatString.is_template_text('%test%'))
        self.assertFalse(TemplateFormatString.is_template_text('%%'))
        self.assertFalse(TemplateFormatString.is_template_text('% and 42%'))
