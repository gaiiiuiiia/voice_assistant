from typing import AnyStr
from typing import Optional

import requests
import json
import logging

from app.core.text_generators.text_generator_base import TextGeneratorBase

logger = logging.getLogger(__name__)


class GPT2Handler(TextGeneratorBase):

    def __init__(self, url: AnyStr) -> None:
        self._url = url

    def generate(self, text: AnyStr) -> Optional[AnyStr]:
        data = {
            'text': text,
        }

        try:
            logger.info(f'Отправка запроса на %s' % self._url)
            response = requests.post(self._url, data=data)
        except Exception as e:
            logger.error(f'Возникла ошибка отправки запроса.')
            return

        decoder = json.JSONDecoder()

        try:
            result = decoder.decode(response.text)
        except Exception:
            logger.error(f'Ошибка при попытке декодировать строку ответа %s' % response.text)
            return

        try:
            return result['text']
        except KeyError:
            logger.error(f'Отсутствует обязательный ключ "text" в "%s"' % response.text)
            return
