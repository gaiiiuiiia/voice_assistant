from typing import Optional

import logging
import random

from app.core.perk_manager import PerkManager
from app.core.text_transformers.text_transformer_base import TextTransformerBase
from app.core.text_generators.text_generator_base import TextGeneratorBase

from app.exceptions.response_method_not_found_exception import ResponseMethodNotFoundException
from app.exceptions.text_transform_exception import TextTransformException

logger = logging.getLogger(__name__)


class AssistantManager:
    def __init__(
            self,
            perk_manager: PerkManager,
            text_transformer: TextTransformerBase,
            text_generator: TextGeneratorBase,
            chance_to_ignore_request: float = 0,
    ) -> None:
        self._perk_manager = perk_manager
        self._text_transformer = text_transformer
        self._text_generator = text_generator
        self._chance_to_ignore_request = chance_to_ignore_request

    def process(self, request: str) -> Optional[str]:
        """
        Принимает строку и возвращает сформированный ответ, прогнанный через перк и текстовый трансформер.
        :param request:
        :return:
        Optional[str]
        """

        if random.random() <= self._chance_to_ignore_request:
            # С некоторой вероятностью проигнорируем запрос, запустив пустобрёх
            logger.info(f'Запрос пользователя "%s" проигнорирован, запускается пустобрёх')
            return self._run_talker(request)

        try:
            perk_response = self._perk_manager.process(request)
        except ResponseMethodNotFoundException:
            # Вот тут включается пустобрех
            logger.info(f'Перк не найден, запускается пустобрёх')
            return self._run_talker(request)

        if not perk_response:
            return

        compiled_perk_response = perk_response.compile()

        try:
            transformed_response = self._text_transformer.transform(perk_response)
        except TextTransformException:
            return compiled_perk_response

        compiled_transformed_response = transformed_response.compile()

        logger.info(f'Результат текст-трансформа - было: "%s", стало "%s"'
                    % (compiled_perk_response, compiled_transformed_response))

        return compiled_transformed_response

    def _run_talker(self, text: str) -> Optional[str]:
        generated_text = self._text_generator.generate(text)

        # TODO тут можно прикрутить стандартные фразы, которые буду замещать неловкое молчание.

        return generated_text if generated_text else 'Какая-то ошибка при генерации текста'
