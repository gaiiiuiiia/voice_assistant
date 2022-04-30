import os


def get_path(path: str) -> str:
    return os.sep.join(path.split('.'))


LOG_DIR = 'app.logs'

PERK_DIRECTORY = 'app.perks'
