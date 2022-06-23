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

        import pprint
        variants = [
            template.compile() for template in
            [self._word2vec_transformer.transform(
                TemplateFormatString(
                    'сегодня температура %temp%. %feels% как 42 градус цельсия',
                    {'temp': 'хорошая', 'feels': 'ощущается', }
                )
            ) for _ in range(3)]
        ]

        pprint.pprint(variants)
