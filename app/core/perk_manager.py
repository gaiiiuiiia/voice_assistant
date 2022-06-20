from typing import Optional
from typing import Tuple

import logging

from app.core.perk_loader import PerkLoader
from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString
from app.exceptions.response_method_not_found_exception import ResponseMethodNotFoundException

logger = logging.getLogger(__name__)


class PerkManager:
    def __init__(self, perk_loader: PerkLoader) -> None:
        self._perk_loader = perk_loader
        self._perks = self._perk_loader.load()

    def process(self, text: str) -> Optional[TemplateFormatString]:
        """
        Принимает строку и отправляет ее методу перка, если данная строка сопоставима с методом.
        Иначе возвращает Null - ни один метод перков не может обработать данную строку.
        :param text: строка запроса.
        :return:
        Optional[TemplateFormatString]
        """
        try:
            perk_method, keywords = self._match_perk_method(text)
        except TypeError:
            raise ResponseMethodNotFoundException('Не найден метод, отвечающий запросу "%s"' % text)

        query = self._parse_query_from_text_by_keywords(text, keywords)

        try:
            if query:
                logger.info('Будет вызван метод "%s" с аргументом "%s"' % (perk_method.__name__, query))
                result = perk_method(query)
            else:
                logger.info('Будет вызван метод "%s" без аргументов' % perk_method.__name__)
                result = perk_method()

        except Exception:
            logger.exception('Исключение при вызове метода "%s" с аргументом "%s"' % (perk_method.__name__, query))
            return

        return result

    def _match_perk_method(self, text: str) -> Optional[Tuple[callable, list]]:
        """
        Вернуть метод, который должен быть вызван, основываясь на заданном тексте и список keywords этого метода.
        :param text: текстовый запрос.
        :return:
        Optional[Tuple[callable, list]]
        """

        for perk in self._perks:
            perk_and_keywords = self.__get_perk_method_name_and_keywords(perk, text)

            if perk_and_keywords:
                perk_method, keywords = perk_and_keywords
                return getattr(perk, perk_method), keywords

    @staticmethod
    def __get_perk_method_name_and_keywords(perk: PerkBase, text: str) -> Optional[Tuple[str, list]]:
        for method_name, keywords in perk.get_manifest_keywords().items():
            for keyword in keywords:
                if keyword in text:
                    return method_name, keywords

    @staticmethod
    def _parse_query_from_text_by_keywords(text: str, keywords: list) -> str:
        for keyword in keywords:
            if keyword in text:
                return text.split(keyword, 1)[1].strip()

        return text
