from app.exceptions.exception_base import ExceptionBase


class ModelExceptionBase(ExceptionBase):
    def __init__(self, message: str = '', *args, **kwargs) -> None:
        message = f'Ошибка файла модели. {message}'
        super().__init__(message, *args, **kwargs)
