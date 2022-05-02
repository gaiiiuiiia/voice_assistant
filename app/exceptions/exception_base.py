import logging

from app.interfaces.loggable_interface import LoggableInterface


class ExceptionBase(Exception, LoggableInterface):

    def __init__(self, message: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.log(message)

    def log(self, message: str) -> None:
        logging.getLogger(__name__).info(f'Exception %s: %s' % (self.__class__.__name__, message))
