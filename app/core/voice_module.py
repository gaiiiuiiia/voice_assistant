import logging
import os
from typing import Optional

import pygame.mixer as pgmixer
import pygame.time as pgtime
import pyttsx3

import app.config as config
from app.core.assistant_manager import AssistantManager
from app.core.voice_recorder import VoiceRecorder

logger = logging.getLogger(__name__)


class Speaker:

    TTS_RATE = 90
    TEMPORARY_SPEECH_FILE = '__temp.mp3'

    def __init__(self) -> None:
        self._speaker = self.__init_pyttsx()
        pgmixer.init()

    def say(self, text: str) -> None:
        self.__make_sound_file(text)
        self.__play_sound_file()
        self.__delete_sound_file()

    def __make_sound_file(self, text: str) -> None:
        self._speaker.save_to_file(text, self.TEMPORARY_SPEECH_FILE)
        self._speaker.runAndWait()

    def __play_sound_file(self) -> None:
        pgtime.wait(100)
        sounda = pgmixer.Sound(self.TEMPORARY_SPEECH_FILE)
        sounda.play()
        pgtime.wait(int(sounda.get_length() * 1000))

    def __delete_sound_file(self) -> None:
        if os.path.exists(self.TEMPORARY_SPEECH_FILE):
            os.remove(self.TEMPORARY_SPEECH_FILE)

    def __init_pyttsx(self) -> pyttsx3.Engine:
        speaker = pyttsx3.init()
        speaker.setProperty('rate', self.TTS_RATE)
        speaker.setProperty('voice', 'russian')

        return speaker


class VoiceModule:
    def __init__(self, assistant_manager: AssistantManager) -> None:
        self._assistant_manager = assistant_manager
        self._voice_recorder = VoiceRecorder()
        self._speaker = Speaker()

    def listen(self) -> None:
        logger.info('Запуск службы голосового модуля. Слушаю окружение')
        while True:
            context = self._voice_recorder.record()
            response = self._process_context(context)
            logger.info(f'Результат %s', response)

            if response:
                self._speaker.say(response)
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
        self._speaker.say(response)
        print(f'вход: %s \nвыход: %s' % (context, response))
