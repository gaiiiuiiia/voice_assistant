import logging

import app.config as config
from app.core.assistant_manager import AssistantManager
from app.core.perk_loader import PerkLoader
from app.core.perk_manager import PerkManager
from app.core.perk_validator import PerkValidator
from app.core.speaker_modules.rhvoice_speaker import RHVoiceOrator
from app.core.speaker_modules.rhvoice_speaker import RHVoiceRestRequestSender
from app.core.speaker_modules.rhvoice_speaker import RHVoiceSpeaker
from app.core.text_generators.gpt2.gpt2_handler import GPT2Handler
from app.core.text_transformers.word2vec.word2vec_transformer import Word2VecTransformer
from app.core.voice_module import VoiceModule


def main() -> None:
    init_logger()

    validator = PerkValidator()
    perk_loader = PerkLoader(validator, config.get_path_os_sep(config.PERK_DIR))
    perk_manager = PerkManager(perk_loader)
    text_transformer = Word2VecTransformer(
        config.get_path_os_sep(config.NAVEC_MODEL_PATH),
        config.ANNOY_N_TREES,
        config.ANNOY_METRICS_NAME,
        config.get_path_os_sep(config.ANNOY_FILE_PATH)
    )
    gpt2 = GPT2Handler(config.GPT2_SERVER_URL)
    assistant_manager = AssistantManager(
        perk_manager,
        text_transformer,
        gpt2,
        config.CHANCE_TO_IGNORE_REQUEST
    )
    rhvoice_orator = RHVoiceOrator(
        config.RHVOICE_ORATOR_NAME,
        'mp3',
        config.RHVOICE_ORATOR_RATE,
        config.RHVOICE_ORATOR_PITCH,
        config.RHVOICE_ORATOR_VOLUME
    )
    request_sender = RHVoiceRestRequestSender(
        config.RHVOICE_SERVICE_NAME,
        config.RHVOICE_SERVICE_PORT,
        rhvoice_orator
    )
    speaker = RHVoiceSpeaker(request_sender, rhvoice_orator)
    voice_module = VoiceModule(assistant_manager, speaker)

    sentence = 'шарик как дела'
    voice_module.test(sentence)
    # voice_module.listen()


def init_logger() -> None:
    logging.basicConfig(filename=config.get_path_os_sep(config.LOG_DIR) + '/log.log',
                        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                        level=logging.INFO)

    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    # file_handler = logging.FileHandler(config.get_path(config.LOG_DIR) + '/log.log')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)


if __name__ == '__main__':
    main()
