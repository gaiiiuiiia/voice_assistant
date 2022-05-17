from abc import ABCMeta
from abc import abstractmethod

from app.core.template_format_string import TemplateFormatString


class TextTransformerBase(metaclass=ABCMeta):

    @abstractmethod
    def transform(self, text_format_data: TemplateFormatString) -> str:
        pass
