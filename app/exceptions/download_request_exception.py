from app.exceptions.model_exception_base import ModelExceptionBase


class DownloadRequestException(ModelExceptionBase):
    def __init__(self, model_name: str, *args, **kwargs) -> None:
        message = self._get_message(model_name)
        super().__init__(message, *args, **kwargs)

    @staticmethod
    def _get_message(file_name: str) -> str:
        return f'Ошибка при попытке получить данные для скачивания "{file_name}".'
