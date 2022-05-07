from typing import Any

from abc import ABCMeta
from abc import abstractmethod

import numpy


class VectorSpace(metaclass=ABCMeta):
    @abstractmethod
    def get_elements(self) -> numpy.ndarray:
        """
        Вернуть набор элементов в пространстве.
        Элемент, это объект, который характеризует вектор.
        :return:
        numpy.ndarray
        """
        pass

    @abstractmethod
    def get_vector_of_element(self, element: Any) -> numpy.ndarray:
        """
        Вернуть вектор, который представляет элемент.
        :return:
        numpy.ndarray
        """
        pass

    @abstractmethod
    def get_vector_dimension(self) -> int:
        """
        Вернуть размер вектора в пространстве.
        :return:
        int
        """
        pass
