import logging
from typing import Optional

import app.config as config
from app.core.assistant_manager import AssistantManager
from app.core.speaker_modules.speaker_base import SpeakerBase
from app.core.voice_recorder import VoiceRecorder

logger = logging.getLogger(__name__)


class VoiceModule:
    def __init__(
            self,
            assistant_manager: AssistantManager,
            speaker: SpeakerBase) -> None:
        self._assistant_manager = assistant_manager
        self._voice_recorder = VoiceRecorder()
        self._speaker = speaker

    def listen(self) -> None:
        logger.info('Запуск службы голосового модуля. Слушаю окружение')
        while True:
            context = self._voice_recorder.record()
            response = self._process_context(context)
            logger.info(f'Результат %s', response)

            if response:
                self._speaker.speak(response)
                print(f'вход: %s \nвыход: %s' % (context, response))

    def _process_context(self, context: str) -> Optional[str]:
        # TODO вынести это в другой модуль. тк голосовой модуль не должен заниматься обработкой запроса
        if config.WAKE_WORD in context:
            logger.info(f'Обнаружен wake-word "%s" в контексте "%s"' % (config.WAKE_WORD, context))
            request = self._get_request_from_context(context)

            if request:
                logger.info(f'Передаю запрос "%s" ассистенту' % request)
                return self._assistant_manager.process(request)

    @staticmethod
    def _get_request_from_context(context: str) -> str:
        split_context = context.split(config.WAKE_WORD)
        split_context.pop(0)
        return ' '.join(split_context).strip()

    def test(self, context: str) -> None:
        response = self._process_context(context)
        self._speaker.speak(response)
        print(f'вход: %s \nвыход: %s' % (context, response))
