import logging

import app.config as config
from app.core.perk_loader import PerkLoader
from app.core.perk_validator import PerkValidator


def main() -> None:
    init_logger()

    validator = PerkValidator()
    loader = PerkLoader(validator, config.get_path(config.PERK_DIRECTORY))
    perks = loader.load()


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
