import sounddevice as sd
import queue
import vosk
import json

import app.config as config


class VoiceRecorder:

    SAMPLERATE = 44100
    BLOCK_SIZE = 8000
    CHANNELS = 1

    def __init__(self) -> None:
        self.q = queue.Queue()
        self.model = vosk.Model(config.VOSK_MODEL_DIR)
        self.recorder = vosk.KaldiRecognizer(self.model, self.SAMPLERATE)

    def record(self) -> str:
        with sd.RawInputStream(samplerate=self.SAMPLERATE, blocksize=self.BLOCK_SIZE, device=None, dtype='int16',
                               channels=self.CHANNELS, callback=self._callback):
            while True:
                data = self.q.get()
                if self.recorder.AcceptWaveform(data):
                    recognized = self.recorder.Result()
                    recognized = json.loads(recognized)
                    recognized_text = recognized['text']

                    if recognized_text:
                        return recognized_text

    def _callback(self, data, frames, time, status) -> None:
        self.q.put(bytes(data))
