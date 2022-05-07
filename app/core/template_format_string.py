from typing import Dict
import re


class TemplateFormatString:
    """
    Класс, представляющий собой шаблонную строку и словарь шаблон-значение.
    "Здесь будет %text%", {text: 'город-сад'}
    """

    TEMPLATE_LEFT_BOUNDARY = '%'
    TEMPLATE_RIGHT_BOUNDARY = '%'

    def __init__(self, text: str, values: Dict = None) -> None:
        self._text = text
        self._values = values if type(values) is dict else {}

    def compile(self) -> str:
        """
        Вернуть отформатированную строку со вставленными шаблонными значениями.
        :return:
        str
        """

        compiled_text = self._text
        for key, value in self._values.items():
            compiled_text = re.sub(
                r'{lft}{key}{rgt}'.format(
                    key=key,
                    lft=self.TEMPLATE_LEFT_BOUNDARY,
                    rgt=self.TEMPLATE_RIGHT_BOUNDARY
                ),
                value,
                compiled_text,
                flags=re.IGNORECASE)

        return compiled_text

    @property
    def text(self) -> str:
        return self._text

    @property
    def values(self) -> dict:
        return self._values

    @classmethod
    def is_template_text(cls, text: str) -> bool:
        """
        Проверить, является ли строка шаблоном.
        :param text:
        :return:
        bool
        """

        return bool(
            re.match(
                r'^{lft}.+{rgt}$'.format(
                    lft=cls.TEMPLATE_LEFT_BOUNDARY,
                    rgt=cls.TEMPLATE_RIGHT_BOUNDARY
                ),
                text,
                flags=re.IGNORECASE
            )
        )
