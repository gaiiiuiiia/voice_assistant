import logging

import app.config as config
from app.core.voice_recorder import VoiceRecorder
from app.core.perk_manager import PerkManager

logger = logging.getLogger(__name__)


class VoiceModule:

    def __init__(self, perk_manager: PerkManager) -> None:
        self._perk_manager = perk_manager
        self._voice_recorder = VoiceRecorder()

    def listen(self) -> None:
        logger.info('Запуск службы голосового модуля. Слушаю окружение')
        while True:
            context = self._voice_recorder.record()
            self._process_context(context)

    def _process_context(self, context: str) -> None:
        if config.WAKE_WORD in context:
            logger.info(f'Обнаружен wake-word в контексте "%s"' % context)
            request = context.split(config.WAKE_WORD)[1]
            if request:
                logger.info(f'Передаю запрос "%s" менеджеру перков' % request)
                self._perk_manager.process(request)

    def test(self, context: str) -> None:
        self._process_context(context)
