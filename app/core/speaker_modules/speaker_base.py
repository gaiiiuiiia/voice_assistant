from abc import ABCMeta, abstractmethod


class SpeakerBase(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def speak(self, text: str) -> None:
        pass
