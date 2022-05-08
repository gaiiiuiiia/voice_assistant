import logging
import random
import re
import string
from typing import Literal

import nltk

from app.core.template_format_string import TemplateFormatString
from app.core.text_transformers.text_transformer_base import TextTransformerBase
from app.core.text_transformers.word2vec.mannoy import Mannoy
from app.core.text_transformers.word2vec.navec_embeddings import NavecEmbeddings

logger = logging.getLogger(__name__)


class Word2VecTransformer(TextTransformerBase):

    # Случайное окно (от и до), в котором выбирается похожие слова. Правая граница не учитывается
    CLOSEST_WORD_WINDOW = (3, 8)

    def __init__(
            self,
            navec_path: str,
            annoy_n_trees: int,
            annoy_metrics_name: Literal["angular", "euclidean", "manhattan", "hamming", "dot"],
            annoy_file_path: str
    ) -> None:

        vector_space = NavecEmbeddings(navec_path)
        self._mannoy = Mannoy(vector_space, annoy_n_trees, annoy_metrics_name, annoy_file_path)

    def transform(
            self,
            template_format_string: TemplateFormatString,
            language: str = 'russian'
    ) -> TemplateFormatString:

        sentences = nltk.sent_tokenize(template_format_string.text)
        result = '. '.join([self._transform_sentence(sentence, language) for sentence in sentences])

        return TemplateFormatString(result, template_format_string.values)

    def _transform_sentence(self, sentence: str, language: str) -> str:
        try:
            stop_words = nltk.corpus.stopwords.words(language)
        except Exception:
            logger.warning(f'В модуле %s не найдены стоп-слова для языка %s' % (self.__class__.__name__, language))
            stop_words = []
        tokens = [self.__strip_token(token) for token in sentence.split()]

        return ' '.join(
            map(
                lambda token: self.__get_random_closest_word(token)
                if token not in stop_words and not TemplateFormatString.is_template_text(token)
                else token,
                tokens
            )
        )

    def __get_random_closest_word(self, word: str) -> str:
        closest_words = self._mannoy.get_n_closest_elements(word, random.choice(range(*self.CLOSEST_WORD_WINDOW)))

        return random.choice(closest_words)

    @staticmethod
    def __strip_token(token: str) -> str:
        punct_without_lft_boundary = re.sub(TemplateFormatString.TEMPLATE_LEFT_BOUNDARY, '', string.punctuation)
        punct_without_rgt_boundary = re.sub(TemplateFormatString.TEMPLATE_RIGHT_BOUNDARY, '', string.punctuation)

        token = token.lstrip(punct_without_lft_boundary)
        token = token.rstrip(punct_without_rgt_boundary)

        return token



