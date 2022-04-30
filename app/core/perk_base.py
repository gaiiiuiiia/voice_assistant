from __future__ import annotations
from typing import Dict
from typing import List

from abc import ABCMeta
from abc import abstractmethod


class PerkBase(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_manifest(cls) -> Dict:
        pass

    def get_manifest_methods(self) -> List[str]:
        """
        Вернуть список названий методов в перке в соответствии с манифестом.
        :return:
        List[str] - список названий методов из манифеста
        """
        return self.get_manifest()['methods'].keys()

    def get_manifest_keywords(self) -> Dict[str, list]:
        """
        Вернуть хеш вида название метода - список ключевых слов.
        :return:
        Dict[str, list] - хеш вида название перка - список ключевых слов
        """

        method_keywords_hash = {}

        for method, params in self.get_manifest()['methods'].items():
            method_keywords_hash[method] = params['keywords']

        return method_keywords_hash

    def __str__(self) -> str:
        return self.__class__.__name__
