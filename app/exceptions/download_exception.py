from app.exceptions.model_exception_base import ModelExceptionBase


class DownloadException(ModelExceptionBase):
    def __init__(self, file_name: str, *args, **kwargs) -> None:
        message = self._get_message(file_name)
        super().__init__(message, *args, **kwargs)

    @staticmethod
    def _get_message(file_name: str) -> str:
        return f'Ошибка при скачивании файла "{file_name}".'
