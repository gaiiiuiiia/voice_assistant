from typing import Optional

import logging

from app.core.perk_loader import PerkLoader
from app.core.perk_base import PerkBase

logger = logging.getLogger(__name__)


class PerkManager:
    def __init__(self, perk_loader: PerkLoader) -> None:
        self._perk_loader = perk_loader
        self._perks = self._perk_loader.load()

    def process(self, text: str) -> Optional[str]:
        perk_method = self._match_perk_method(text)

        # TODO проверить, а нужны ли параметры методу
        return perk_method(text)

    def _match_perk_method(self, text: str) -> Optional[callable]:
        """
        Вернуть метод, который должен быть вызван, основываясь на заданном тексте.
        :param text: текстовый запрос.
        :return:
        Callable - метод перка, отвечающий запросу.
        """

        for perk in self._perks:
            perk_method = self.__get_perk_method_name(perk, text)

            if perk_method:
                return getattr(perk, perk_method)

    @staticmethod
    def __get_perk_method_name(perk: PerkBase, text: str) -> callable:
        for method_name, keywords in perk.get_manifest_keywords().items():
            for keyword in keywords:
                if keyword in text:
                    return method_name
