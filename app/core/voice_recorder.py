import sounddevice as sd
import queue
import vosk
import json

import app.config as config


class VoiceRecorder:

    SAMPLERATE = 44100
    BLOCK_SIZE = 8000
    CHANNELS = 1
    DTYPE = 'int16'

    def __init__(self) -> None:
        self._queue = queue.Queue()
        model = vosk.Model(config.get_path_os_sep(config.VOSK_MODEL_DIR))
        self._recognizer = vosk.KaldiRecognizer(model, self.SAMPLERATE)

    def record(self) -> str:
        with sd.RawInputStream(samplerate=self.SAMPLERATE, blocksize=self.BLOCK_SIZE, device=None, dtype=self.DTYPE,
                               channels=self.CHANNELS, callback=self._callback):
            while True:
                data = self._queue.get()
                if self._recognizer.AcceptWaveform(data):
                    recognized = self._recognizer.Result()
                    recognized = json.loads(recognized)
                    recognized_text = recognized['text']

                    if recognized_text:
                        return recognized_text

    def _callback(self, data, frames, time, status) -> None:
        self._queue.put(bytes(data))
