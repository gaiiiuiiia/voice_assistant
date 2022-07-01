import logging
import os
from dataclasses import dataclass

import requests
from tqdm import tqdm

import app.config as config
from app.exceptions.download_model_exception import DownloadModelException
from app.interfaces.downloader_interface import DownloaderInterface
from app.interfaces.download_informer_interface import DownloadInformerInterface
from main import init_logger

init_logger()
logger = logging.getLogger(__name__)


def print_separate(separate_str: str = '=' * 42) -> callable:
    def decorator(func: callable) -> callable:
        def wrapper(*args, **kwargs):
            print(separate_str)
            res = func(*args, **kwargs)
            print(separate_str)
            return res

        return wrapper

    return decorator


@dataclass(slots=True, frozen=True)
class Model:
    name: str
    directory: str
    path: str
    download_link: str

    def __str__(self) -> str:
        return self.name


class ConsoleDownloadInformer(DownloadInformerInterface):
    def __init__(self, model: Model) -> None:
        self._model = model

    @print_separate
    def inform_already_exist(self) -> None:
        print(f'Модель {self._model.name} уже существует по пути {self._model.path}.'
              f' Повторная загрузка не будет осуществлена.')

    @print_separate
    def inform_before_download(self) -> None:
        print(f'Будет закачана модель: {self._model.name}.')
        print(f'Откуда: {self._model.download_link}.')
        print(f'Место назначения: {self._model.path}.')

    @print_separate
    def inform_after_download(self) -> None:
        print(f'Модель успешно скачана. Расположение: {self._model.path}')

    @print_separate
    def inform_download_error(self) -> None:
        print(f'Ошибка при скачивании модели {self._model.name}')


class ModelDownloader(DownloaderInterface):
    def __init__(self, model: Model) -> None:
        self._model = model

    def download(self) -> None:
        """
        Скачивает данные модели из Интернета.
        :return:
        """
        if not os.path.exists(self._model.directory):
            os.makedirs(self._model.directory, exist_ok=True)

        with open(self._model.path, 'wb') as file:
            try:
                response = requests.get(self._model.download_link, stream=True)
            except Exception:
                raise DownloadModelException(self._model.name)

            file_size = int(response.headers["content-length"])
            chunk_size = 1000
            with tqdm(ncols=100, desc=f'Скачивается {self._model.name}', total=file_size, unit_scale=True) as pbar:
                # 1k for chunk_size, since Ethernet packet size is around 1500 bytes
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
                    pbar.update(chunk_size)


class ModelDownloadHandler:
    def __init__(
            self,
            downloader: DownloaderInterface,
            informer: DownloadInformerInterface
    ) -> None:
        self._downloader = downloader
        self._informer = informer

    def handle_download(self) -> None:
        self._informer.inform_before_download()
        try:
            self._downloader.download()
        except DownloadModelException:
            self._informer.inform_download_error()
            return

        self._informer.inform_after_download()


def main() -> None:
    models = [
        Model(
            config.VOSK_MODEL,
            config.VOSK_MODEL_DIR,
            config.VOSK_MODEL_PATH,
            config.DOWNLOAD_MODEL_LINK_VOSK
        ),
        Model(
            config.NAVEC_MODEL,
            config.NAVEC_MODEL_DIR,
            config.NAVEC_MODEL_PATH,
            config.DOWNLOAD_MODEL_LINK_NAVEC
        )
    ]

    for model in models:
        informer = ConsoleDownloadInformer(model)

        if os.path.exists(model.path):
            informer.inform_already_exist()
            continue

        downloader = ModelDownloader(model)
        model_download_handler = ModelDownloadHandler(downloader, informer)
        model_download_handler.handle_download()


if __name__ == '__main__':
    main()
