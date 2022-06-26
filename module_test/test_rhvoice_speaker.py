import unittest

from app.core.speaker_modules.rhvoice_speaker import RHVoiceSpeaker
from app.core.speaker_modules.rhvoice_speaker import RHVoiceRestRequestSender
from app.core.speaker_modules.rhvoice_speaker import RHVoiceOrator
import app.config as config


class TestRHVoiceSpeaker(unittest.TestCase):

    def test_say(self) -> None:
        return
        # rhvoice_orator = RHVoiceOrator(
        #     config.RHVOICE_ORATOR_NAME,
        #     'mp3',
        #     config.RHVOICE_ORATOR_RATE,
        #     config.RHVOICE_ORATOR_PITCH,
        #     config.RHVOICE_ORATOR_VOLUME
        # )
        # request_sender = RHVoiceRestRequestSender(
        #     config.RHVOICE_SERVICE_NAME,
        #     config.RHVOICE_SERVICE_PORT,
        #     rhvoice_orator
        # )
        # speaker = RHVoiceSpeaker(request_sender, rhvoice_orator)
        # rhvoice_speaker.speak('привет мир!')

