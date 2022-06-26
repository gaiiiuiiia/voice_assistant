import os

import pygame.mixer as pgmixer
import pygame.time as pgtime
import pyttsx3

from app.core.speaker_modules.speaker_base import SpeakerBase


class Pyttsx3Speaker(SpeakerBase):

    TTS_RATE = 90
    TEMPORARY_SPEECH_FILE = '__temp.mp3'

    def __init__(self) -> None:
        super().__init__()
        self._speaker = self.__init_pyttsx()
        pgmixer.init()

    def speak(self, text: str) -> None:
        self.__make_sound_file(text)
        pgtime.wait(200)
        self.__play_sound_file()
        self.__delete_sound_file()

    def __make_sound_file(self, text: str) -> None:
        self._speaker.save_to_file(text, self.TEMPORARY_SPEECH_FILE)
        self._speaker.runAndWait()

    def __play_sound_file(self) -> None:
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
