import logging

from app.interfaces.loggable_interface import LoggableInterface

logger = logging.getLogger(__name__)


class ExceptionBase(Exception, LoggableInterface):

    def __init__(self, message: str = '', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.log(message)

    def log(self, message: str) -> None:
        logger.exception(f'Exception %s: %s' % (self.__class__.__name__, message))
