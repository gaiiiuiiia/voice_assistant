import logging
import random
import re

from typing import Literal

from app.core.template_format_string import TemplateFormatString
from app.core.text_transformers.text_transformer_base import TextTransformerBase
from app.core.text_transformers.word2vec.mannoy import Mannoy
from app.core.text_transformers.word2vec.navec_embeddings import NavecEmbeddings

logger = logging.getLogger(__name__)


class Word2VecTransformer(TextTransformerBase):

    # Случайное окно (от и до), в котором выбирается похожие слова. Правая граница не учитывается
    CLOSEST_WORD_WINDOW = (3, 7)

    def __init__(
            self,
            navec_path: str,
            annoy_n_trees: int,
            annoy_metrics_name: Literal["angular", "euclidean", "manhattan", "hamming", "dot"],
            annoy_file_path: str
    ) -> None:

        vector_space = NavecEmbeddings(navec_path)
        self._mannoy = Mannoy(vector_space, annoy_n_trees, annoy_metrics_name, annoy_file_path)

    def transform(self, template_formatted_string: TemplateFormatString) -> TemplateFormatString:

        old_values = template_formatted_string.values
        new_values = {}

        for key in old_values.keys():
            new_values[key] = self.__get_random_closest_word(old_values[key])

        return TemplateFormatString(template_formatted_string.text, new_values)

    def __get_random_closest_word(self, word: str) -> str:
        closest_words = self._mannoy.get_n_closest_elements(word, random.choice(range(*self.CLOSEST_WORD_WINDOW)))

        return random.choice(closest_words)
