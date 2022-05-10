import os


def get_path_os_sep(path: str) -> str:
    return os.sep.join(path.split('/'))


WAKE_WORD = 'шарик'

CHANCE_TO_IGNORE_REQUEST = 0.2

GPT2_SERVER_URL = 'http://gpt2web:8000/gpt2/query/'

# Количество деревьев в лесу Annoy (желательно степень двойки)
ANNOY_N_TREES = 256

# Путь к файлу Annoy. Тут хранятся построенные леса
ANNOY_FILE_PATH = 'app/models/annoy_trees.ann'

# Метрика близости Annoy. "angular", "euclidean", "manhattan", "hamming", "dot"
ANNOY_METRICS_NAME = 'euclidean'

NAVEC_FILE_PATH = 'app/models/navec/navec_hudlit_v1_12B_500K_300d_100q.tar'

LOG_DIR = 'app/logs'

PERK_DIRECTORY = 'app/perks'

VOSK_MODEL_DIR = 'app/models/vosk-model-small-ru-0.22'
