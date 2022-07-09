import logging
import os
import shutil
from dataclasses import dataclass

import requests
from tqdm import tqdm

import app.config as config
from app.exceptions.download_exception import DownloadException
from app.exceptions.download_request_exception import DownloadRequestException
from app.exceptions.extract_file_exception import ExtractFileException
from main import init_logger

init_logger()
logger = logging.getLogger(__name__)


def print_separate_decorator(separate_str: str = '=' * 42) -> callable:
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
    need_to_extract: bool

    def __str__(self) -> str:
        return self.name


class ConsoleInformer:
    @staticmethod
    @print_separate_decorator()
    def inform_before_download(file_name: str, file_path: str, download_link: str) -> None:
        print(f'Будет закачан файл: "{file_name}".')
        print(f'Откуда: "{download_link}".')
        print(f'Место назначения: "{file_path}".')

    @staticmethod
    @print_separate_decorator()
    def inform_after_download(file_path: str) -> None:
        print(f'Файл успешно скачан. Расположение: "{file_path}".')

    @staticmethod
    @print_separate_decorator()
    def inform_download_error(file_name: str) -> None:
        print(f'Ошибка при скачивании "{file_name}".')

    @staticmethod
    @print_separate_decorator()
    def inform_extract_error(from_path: str, to_path: str) -> None:
        print(f'Ошибка распаковки файла из "{from_path}" в "{to_path}".')

    @staticmethod
    @print_separate_decorator()
    def inform_after_extract(to_path: str) -> None:
        print(f'Файл был успешно распакован по пути "{to_path}".')


def download(link: str, download_file_path: str) -> None:
    """
    Скачивает данные модели из Интернета.
    :return:
    """
    download_file_dir = os.path.dirname(download_file_path)
    download_file_name = download_file_path.split(os.sep)[-1]

    if not os.path.exists(download_file_dir):
        os.makedirs(download_file_dir, exist_ok=True)

    try:
        with open(download_file_path, 'wb') as file:
            try:
                response = requests.get(link, stream=True)
            except Exception:
                raise DownloadRequestException(download_file_name)
            file_size = int(response.headers["content-length"])
            chunk_size = 1024

            with tqdm(ncols=150, desc=f'Скачивается {download_file_name}', total=file_size, unit_scale=True) as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
                    pbar.update(chunk_size)
    except Exception:
        raise DownloadException(download_file_path)


class FileExtractor:
    ALLOWED_MIMETYPES = [
        'application/zip',
    ]

    def __init__(self, extract_from: str, extract_to: str) -> None:
        self._extract_from = extract_from
        self._extract_to = extract_to

    def extract(self) -> None:
        if not os.path.exists(self._extract_from):
            raise ExtractFileException(f'Файл "{self._extract_from}" не существует.')

        if not self._can_be_extracted():
            raise ExtractFileException(f'Файл "{self._extract_from}" не может быть распакован.')

        if not os.path.exists(self._extract_to):
            os.makedirs(self._extract_to, exist_ok=True)

        try:
            self._do_extract()
        except FileExistsError:
            raise ExtractFileException(f'В директории "{self._extract_to}" уже существует указанный файл.')

    def _do_extract(self) -> None:
        import zipfile

        with (zipfile.ZipFile(self._extract_from, 'r')) as zip_file:
            zip_file.extractall(self._extract_to)

    def _can_be_extracted(self) -> bool:
        import magic
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(self._extract_from)

        return mime_type in self.ALLOWED_MIMETYPES


def main() -> None:
    models = [
        Model(
            config.VOSK_MODEL,
            config.VOSK_MODEL_DIR,
            config.VOSK_MODEL_PATH,
            config.DOWNLOAD_MODEL_LINK_VOSK,
            config.VOSK_MODEL_NEED_EXTRACT,
        ),
        Model(
            config.NAVEC_MODEL,
            config.NAVEC_MODEL_DIR,
            config.NAVEC_MODEL_PATH,
            config.DOWNLOAD_MODEL_LINK_NAVEC,
            config.NAVEC_MODEL_NEED_EXTRACT,
        )
    ]

    for model in models:
        download_path = os.sep.join([config.get_path_os_sep(config.DOWNLOAD_DIR), model.name])

        if not os.path.exists(download_path):
            try:
                ConsoleInformer.inform_before_download(model.name, download_path, model.download_link)
                download(model.download_link, download_path)
            except (DownloadException, DownloadRequestException):
                ConsoleInformer.inform_download_error(model.name)
                continue
            ConsoleInformer.inform_after_download(download_path)

        if model.need_to_extract:
            extractor = FileExtractor(download_path, model.directory)
            try:
                extractor.extract()
            except ExtractFileException:
                ConsoleInformer.inform_extract_error(download_path, model.path)
            ConsoleInformer.inform_after_extract(model.path)
            continue

        if not os.path.exists(model.directory):
            os.makedirs(model.directory, exist_ok=True)

        os.replace(download_path, model.path)
        shutil.rmtree(config.DOWNLOAD_DIR)


if __name__ == '__main__':
    main()
