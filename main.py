import logging

import app.config as config
from app.core.perk_loader import PerkLoader
from app.core.perk_validator import PerkValidator
from app.core.voice_module import VoiceModule
from app.core.perk_manager import PerkManager


def main() -> None:
    init_logger()

    validator = PerkValidator()
    perk_loader = PerkLoader(validator, config.get_path(config.PERK_DIRECTORY))
    perk_manager = PerkManager(perk_loader)
    voice_module = VoiceModule(perk_manager)

    sentence = 'шарик скажи какая сейчас погода в казани'
    voice_module.test(sentence)
    # voice_module.listen()


def init_logger() -> None:
    logging.basicConfig(filename=config.get_path(config.LOG_DIR) + '/log.log',
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
