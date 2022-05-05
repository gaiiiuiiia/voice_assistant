from typing import Optional

import logging

from app.core.perk_manager import PerkManager
from app.core.text_transformers.text_transformer_base import TextTransformerBase

from app.exceptions.response_method_not_found_exception import ResponseMethodNotFoundException
from app.exceptions.text_transform_exception import TextTransformException

logger = logging.getLogger(__name__)


class AssistantManager:
    def __init__(self, perk_manager: PerkManager, text_transformer: TextTransformerBase) -> None:
        self._perk_manager = perk_manager
        self._text_transformer = text_transformer

    def process(self, request: str) -> Optional[str]:
        """
        Принимает строку и возвращает сформированный ответ, прогнанный через перк и текстовый трансформер.
        :param request:
        :return:
        Optional[str]
        """
        try:
            perk_response = self._perk_manager.process(request)
        except ResponseMethodNotFoundException:
            # Вот тут включается пустобрех
            logger.info(f'Перк не найден, запускается пустобрёх')
            return 'пустобрёх был тут'

        if not perk_response:
            return

        compiled_perk_response = perk_response.compile()

        try:
            transformed_response = self._text_transformer.transform(perk_response)
        except TextTransformException:
            return compiled_perk_response

        compiled_transformed_response = transformed_response.compile()

        logger.info(f'Результат текст трансформа. было: "%s", стало "%s"'
                    % (compiled_perk_response, compiled_transformed_response))

        return compiled_transformed_response
