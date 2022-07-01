from abc import ABCMeta, abstractmethod


class DownloadInformerInterface(metaclass=ABCMeta):

    @abstractmethod
    def inform_already_exist(self) -> None:
        pass

    @abstractmethod
    def inform_before_download(self) -> None:
        pass

    @abstractmethod
    def inform_after_download(self) -> None:
        pass

    def inform_download_error(self) -> None:
        pass
