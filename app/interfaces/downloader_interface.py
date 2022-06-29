from abc import ABCMeta, abstractmethod


class DownloaderInterface(metaclass=ABCMeta):
    @abstractmethod
    def download(self) -> None:
        pass
