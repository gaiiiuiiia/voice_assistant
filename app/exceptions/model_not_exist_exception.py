from app.exceptions.model_exception_base import ModelExceptionBase

import app.config as config


class ModelNotExistException(ModelExceptionBase):
    def __init__(self, path: str, *args, **kwargs) -> None:
        message = self._get_message(path)
        super().__init__(message, *args, **kwargs)

    @staticmethod
    def _get_message(path: str) -> str:
        return f'Модель "{path}" не найдена. ' \
               f'Попробуйте запустить скрипт {config.get_path_os_sep(config.DOWNLOAD_MODELS_SCRIPT)}.'
