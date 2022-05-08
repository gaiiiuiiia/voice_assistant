import logging

import app.config as config
from app.core.perk_loader import PerkLoader
from app.core.perk_validator import PerkValidator
from app.core.voice_module import VoiceModule
from app.core.perk_manager import PerkManager
from app.core.text_transformers.word2vec.word2vec_transformer import Word2VecTransformer
from app.core.assistant_manager import AssistantManager


def main() -> None:
    init_logger()

    validator = PerkValidator()
    perk_loader = PerkLoader(validator, config.get_path_os_sep(config.PERK_DIRECTORY))
    perk_manager = PerkManager(perk_loader)
    text_transformer = Word2VecTransformer(
        config.get_path_os_sep(config.NAVEC_FILE_PATH),
        config.ANNOY_N_TREES,
        config.ANNOY_METRICS_NAME,
        config.get_path_os_sep(config.ANNOY_FILE_PATH)
    )
    assistant_manager = AssistantManager(perk_manager, text_transformer, config.CHANCE_TO_IGNORE_REQUEST)
    voice_module = VoiceModule(assistant_manager)

    sentence = 'шарик кинь монету'
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
