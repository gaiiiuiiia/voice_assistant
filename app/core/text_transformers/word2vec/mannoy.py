from typing import Any
from typing import List
from typing import Literal
import os

from annoy import AnnoyIndex

from app.core.text_transformers.word2vec.vector_space import VectorSpace


class Mannoy:
    """
    Обёртка над numpy массивом для быстрого поиска элементов
    """
    def __init__(
            self,
            vector_space: VectorSpace,
            n_trees: int,
            metrics: Literal["angular", "euclidean", "manhattan", "hamming", "dot"],
            annoy_file_path: str
    ) -> None:
        self._vector_space = vector_space
        self._annoy = self._init_annoy(n_trees, metrics, annoy_file_path)

    def get_n_closest_elements(
            self,
            element: Any,
            n: int
    ) -> List[Any]:
        """
        Вернуть n ближайших элементов в пространстве по отношению к заданному элементу.
        :param element: элемент пространства.
        :param n: количество ближайших элементов.
        :return:
        List[Any]
        """

        res = self._annoy.get_nns_by_vector(self._vector_space.get_vector_of_element(element), n)

        return [self._vector_space.get_elements()[i] for i in res]

    def _init_annoy(
            self,
            n_trees: int,
            metrics: Literal["angular", "euclidean", "manhattan", "hamming", "dot"],
            file_path: str
    ) -> AnnoyIndex:

        vec_dim = self._vector_space.get_vector_dimension()
        annoy_index = AnnoyIndex(vec_dim, metrics)

        if os.path.exists(file_path):
            annoy_index.load(file_path)
            return annoy_index

        for index, element in enumerate(self._vector_space.get_elements()):
            annoy_index.add_item(index, self._vector_space.get_vector_of_element(element))

        annoy_index.build(n_trees)
        annoy_index.save(file_path)

        return annoy_index
