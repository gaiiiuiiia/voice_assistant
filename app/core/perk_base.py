from __future__ import annotations
from typing import Dict
from typing import List
from typing import Optional

from abc import ABCMeta
from abc import abstractmethod

from app.exceptions.incorrect_perk_class_exception import IncorrectPerkClassException


class PerkBase(metaclass=ABCMeta):

    def __init__(self) -> None:
        self._manifest = self._do_create_manifest()

    @abstractmethod
    def _do_create_manifest(self) -> Dict:
        """
        При создании класса, необходимо указать манифест.
        Метод обязан вернуть словарь вида:
        {
            'name': 'PerkName',
            'methods': {
                'method_name': {
                    'keywords': ['some', 'keywords', ...],
                    'args': [''],
                },
            },
        }
        :return:
        Dict
        """
        pass

    def get_manifest(self) -> Dict:
        return self._manifest

    def get_manifest_methods(self) -> List[str]:
        """
        Вернуть список названий методов в перке в соответствии с манифестом.
        :return:
        List[str] - список названий методов из манифеста
        """
        try:
            return list(self.get_manifest().get('methods').keys())
        except TypeError:
            return []

    def get_manifest_keywords(self) -> Dict[str, list]:
        """
        Вернуть хеш вида название метода - список ключевых слов.
        :return:
        Dict[str, list] - хеш вида название перка - список ключевых слов
        """

        method_keywords_hash = {}

        manifest_methods: dict = self.get_manifest().get('methods')

        if not manifest_methods:
            raise IncorrectPerkClassException

        for method, params in manifest_methods.items():
            keywords = params.get('keywords')
            method_keywords_hash[method] = keywords if keywords else []

        return method_keywords_hash

    def get_method_manifest(self, method_name: str) -> Optional[Dict]:
        try:
            return self.get_manifest().get('methods').get(method_name)
        except TypeError:
            raise IncorrectPerkClassException

    def __str__(self) -> str:
        return self.__class__.__name__
