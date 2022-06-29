import os

import navec
import numpy

from app.core.text_transformers.word2vec.vector_space import VectorSpace
from app.exceptions.model_not_exist_exception import ModelNotExistException


class NavecEmbeddings(VectorSpace):
    def __init__(self, path: str) -> None:
        if not os.path.exists(path):
            raise ModelNotExistException(path)
        self._navec = navec.Navec.load(path)

    def get_elements(self) -> numpy.ndarray:
        return self._navec.vocab.words

    def get_vector_of_element(self, element) -> numpy.ndarray:
        return self._navec[element]

    def get_vector_dimension(self) -> int:
        return self._navec.pq.dim
