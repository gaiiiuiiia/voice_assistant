import os


def get_path_os_sep(path: str) -> str:
    return os.sep.join(path.split('/'))


WAKE_WORD = 'шарик'

LOG_DIR = 'app/logs'

PERK_DIRECTORY = 'app/perks'

VOSK_MODEL_DIR = 'app/models/vosk-model-small-ru-0.22'
