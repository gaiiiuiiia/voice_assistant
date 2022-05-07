from app.core.template_format_string import TemplateFormatString
from app.core.text_transformers.text_transformer_base import TextTransformerBase
from app.core.text_transformers.word2vec.navec_embeddings import NavecEmbeddings
from app.core.text_transformers.word2vec.mannoy import Mannoy

import app.config as config


class Word2VecTransformer(TextTransformerBase):

    def __init__(
            self,
            navec_path: str
    ) -> None:

        vector_space = NavecEmbeddings(navec_path)
        self._mannoy = Mannoy(
            vector_space,
            config.ANNOY_N_TREES,
            config.ANNOY_METRICS_NAME,
            config.ANNOY_FILE_PATH
        )

    def transform(self, text_format_data: TemplateFormatString) -> TemplateFormatString:
        pass

