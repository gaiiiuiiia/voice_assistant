import unittest

from app.core.text_transformers.word2vec.word2vec_transformer import Word2VecTransformer
from app.core.template_format_string import TemplateFormatString
import app.config as config


class TestWord2VecTransformer(unittest.TestCase):

    def setUp(self) -> None:
        self._word2vec_transformer = Word2VecTransformer(
            config.get_path_os_sep(config.NAVEC_FILE_PATH),
            config.ANNOY_N_TREES,
            config.ANNOY_METRICS_NAME,
            config.get_path_os_sep(config.ANNOY_FILE_PATH)
        )

    def test_transform(self) -> None:
        res = self._word2vec_transformer.transform(
            TemplateFormatString(
                'сегодня температура хорошая. ощущается как %temp% %desc%',
                {'temp': '42', 'desc': 'градусов цельсия'}
            )
        ).compile()

        self.assertTrue(True)
