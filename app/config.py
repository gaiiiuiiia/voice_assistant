import os


def get_path_os_sep(path: str) -> str:
    return os.sep.join(path.split('/'))


WAKE_WORD = 'максим'

DEFAULT_WEATHER_LOCATION = 'казань'

CHANCE_TO_IGNORE_REQUEST = 0

GPT2_SERVER_URL = 'http://gpt2web:8000/gpt2/query/'

RHVOICE_SERVICE_NAME = 'rhvoice_rest'  # название сервиса RHVoice в файле docker-compose
RHVOICE_SERVICE_PORT = '8080'  # порт, на котором запущен сервис RHVoice
RHVOICE_ORATOR_NAME = 'artemiy'  # Literal["aleksandr", "anna", "arina", "artemiy", "elena", "irina", "pavel"]
RHVOICE_ORATOR_RATE = 30
RHVOICE_ORATOR_PITCH = 42
RHVOICE_ORATOR_VOLUME = 100

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
# VOSK_MODEL_DIR = 'app/models/vosk-model-ru-0.22'

ASSETS_DIR = 'assets'
