from typing import Optional
import logging

import pyttsx3

import app.config as config
from app.core.voice_recorder import VoiceRecorder
from app.core.assistant_manager import AssistantManager

logger = logging.getLogger(__name__)


class VoiceModule:

    TTS_RATE = 150

    def __init__(self, assistant_manager: AssistantManager) -> None:
        self._assistant_manager = assistant_manager
        self._voice_recorder = VoiceRecorder()
        self._speaker = self.__init_pyttsx()

    def listen(self) -> None:
        logger.info('Запуск службы голосового модуля. Слушаю окружение')
        while True:
            context = self._voice_recorder.record()
            response = self._process_context(context)

            if response:
                # self._speaker.say(response)
                print(f'вход: %s \nвыход: %s', context, response)

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

    def __init_pyttsx(self) -> pyttsx3.Engine:
        speaker = pyttsx3.init()
        speaker.setProperty('rate', self.TTS_RATE)

        return speaker

    def test(self, context: str) -> None:
        self._process_context(context)
