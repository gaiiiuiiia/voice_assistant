from typing import Literal

from app.core.template_format_string import TemplateFormatString
from app.core.text_transformers.text_transformer_base import TextTransformerBase
from app.core.text_transformers.word2vec.navec_embeddings import NavecEmbeddings
from app.core.text_transformers.word2vec.mannoy import Mannoy


class Word2VecTransformer(TextTransformerBase):

    def __init__(
            self,
            navec_path: str,
            annoy_n_trees: int,
            annoy_metrics_name: Literal["angular", "euclidean", "manhattan", "hamming", "dot"],
            annoy_file_path: str
    ) -> None:

        vector_space = NavecEmbeddings(navec_path)
        self._mannoy = Mannoy(
            vector_space,
            annoy_n_trees,
            annoy_metrics_name,
            annoy_file_path
        )

    def transform(self, text_format_data: TemplateFormatString) -> TemplateFormatString:
        return text_format_data

