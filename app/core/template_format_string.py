from typing import Dict
import re


class TemplateFormatString:
    """
    Класс, представляющий собой шаблонную строку и словарь шаблон-значение.
    "Здесь будет {%text%}", {text: 'город-сад'}
    """

    def __init__(self, text: str, args: Dict) -> None:
        self._text = text
        self._args = args

    def compile(self) -> str:
        """
        Вернуть отформатированную строку со вставленными шаблонными значениями.
        :return:
        """
        return 'formatted string is here'

    @property
    def text(self) -> str:
        return self._text

    @property
    def args(self) -> dict:
        return self._args

    @staticmethod
    def is_placeholder_string(text: str) -> bool:
        """
        Проверить, является ли строка шаблоном.
        :param text:
        :return:
        """
        return True

    def __repr__(self) -> str:
        pass
