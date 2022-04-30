from abc import ABCMeta
from abc import abstractmethod


class LoggableInterface(metaclass=ABCMeta):

    @abstractmethod
    def log(self, message: str) -> None:
        pass
