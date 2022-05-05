from typing import Optional

import logging

from app.core.perk_loader import PerkLoader
from app.core.perk_base import PerkBase
from app.core.text_transformers.text_transformer_base import TextTransformerBase
from app.core.template_format_string import TemplateFormatString

logger = logging.getLogger(__name__)


class PerkManager:
    def __init__(self, perk_loader: PerkLoader, text_transformer: TextTransformerBase) -> None:
        self._perk_loader = perk_loader
        self._text_transformer = text_transformer
        self._perks = self._perk_loader.load()

    def process(self, text: str) -> Optional[str]:
        perk_method = self._match_perk_method(text)

        if not perk_method:
            logger.error('Не найден метод, отвечающий запросу "%s"' % text)
            return

        logger.info('Будет вызван метод "%s"' % perk_method.__name__)
        try:
            # TODO проверить, а нужны ли параметры методу
            result = perk_method(text)
        except Exception:
            logger.exception('Исключение при вызове метода "%s"' % perk_method.__name__)
            return

        # TODO пока методы перков возвращают объект
        assert type(result) is TemplateFormatString

        try:
            compiled_text = result.compile()
            logger.info('Результат метода "%s": %s' % (perk_method.__name__, compiled_text))
        except Exception:
            logger.exception(f'Не удалось скомпилировать результат. %s' % result)
            return

        try:
            text_transform = self._text_transformer.transform(result)
        except Exception:
            logger.exception(f'Не удалось трансформировать результат перка %s' % result)
            return compiled_text

        try:
            compiled_text_transform = text_transform.compile()
            logger.info(f'Результат трансформ текста: %s' % compiled_text_transform)
        except Exception:
            logger.exception(f'Не удалось скомпилировать результат после трансформа. %s' % text_transform)
            return compiled_text

        return result

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
