from abc import ABCMeta
from abc import abstractmethod


class TextGeneratorBase(metaclass=ABCMeta):

    @abstractmethod
    def generate(self, text: str) -> str:
        """
        Сгенерировать текст в ответ на заданный текст
        :param text:
        :return:
        str
        """
