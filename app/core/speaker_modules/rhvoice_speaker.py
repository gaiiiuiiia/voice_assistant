import io
import logging
from typing import Literal

import pydub
import requests
from pydub import playback

from app.core.speaker_modules.speaker_base import SpeakerBase

logger = logging.getLogger(__name__)


class RHVoiceOrator:
    def __init__(
            self,
            voice: Literal["aleksandr", "anna", "arina", "artemiy", "elena", "irina", "pavel"],
            format_: Literal["wav", "mp3", "opus", "flac"],
            rate: int,
            pitch: int,
            volume: int
    ) -> None:
        """
        :param voice: имя озвучивающего.
        :param format_: формат, в котором придет файл от сервера.
        :param rate: скорость произношения от 0 до 100 включительно.
        :param pitch: тональность произношения от 0 до 100 включительно.
        :param volume: громкость произношения от 0 до 100 включительно.
        """
        self.__voice = voice
        self.__format = format_
        self.__rate = rate if 0 <= rate <= 100 else 50
        self.__pitch = pitch if 0 <= pitch <= 100 else 50
        self.__volume = volume if 0 <= volume <= 100 else 50

    @property
    def voice(self):
        return self.__voice

    @property
    def format(self):
        return self.__format

    @property
    def rate(self):
        return self.__rate

    @property
    def pitch(self):
        return self.__pitch

    @property
    def volume(self):
        return self.__volume


class RHVoiceRestRequestSender:
    def __init__(
            self,
            service_host: str,
            service_port: str,
            orator: RHVoiceOrator
    ) -> None:
        self.__service_host = service_host
        self.__service_port = service_port
        self.__orator = orator

    def send_request(self, text: str) -> bytes:
        service_url = self.__get_service_url()
        params = {
            'text': text,
            'voice': self.__orator.voice,
            'format': self.__orator.format,
            'rate': self.__orator.rate,
            'pitch': self.__orator.pitch,
            'volume': self.__orator.volume,
        }
        response = requests.get(service_url, params=params, stream=True)
        return response.raw.data
    
    def __get_service_url(self) -> str:
        return f'http://{self.__service_host}:{self.__service_port}/say'


class RHVoiceSpeaker(SpeakerBase):
    def __init__(
            self,
            request_sender: RHVoiceRestRequestSender,
            rhvoice_orator: RHVoiceOrator,
    ) -> None:
        super().__init__()
        self.__request_sender = request_sender
        self.__rhvoice_orator = rhvoice_orator

    def speak(self, text: str) -> None:
        byte_data = self.__request_sender.send_request(text)
        recording = pydub.AudioSegment.from_file(io.BytesIO(byte_data), format=self.__rhvoice_orator.format)
        playback.play(recording)
