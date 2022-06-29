import os


def get_path_os_sep(path: str) -> str:
    return os.sep.join(path.split('/'))


# ===== Assistant Config =====
WAKE_WORD = 'шарик'
DEFAULT_WEATHER_LOCATION = 'казань'
CHANCE_TO_IGNORE_REQUEST = 0
# ============================

# ===== GPT2 Config =====
GPT2_SERVER_URL = 'http://gpt2web:8000/gpt2/query/'
# =======================

# ===== Directory Config =====
PERK_DIR = 'app/perks'
LOG_DIR = 'app/logs'
ASSETS_DIR = 'assets'
MODELS_DIR = 'app/models'
VOSK_MODEL_DIR = f'{MODELS_DIR}/vosk'
NAVEC_MODEL_DIR = f'{MODELS_DIR}/navec'
ANNOY_MODEL_DIR = f'f{MODELS_DIR}/annoy'
# ============================

# ===== Models Config =====
VOSK_MODEL = 'vosk-model-small-ru-0.22'
NAVEC_MODEL = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
VOSK_MODEL_PATH = f'{VOSK_MODEL_DIR}/{VOSK_MODEL}'
NAVEC_MODEL_PATH = f'{NAVEC_MODEL_DIR}/{NAVEC_MODEL}'
# =========================

# ===== RHVoice Config =====
RHVOICE_SERVICE_NAME = 'rhvoice_rest'  # название сервиса RHVoice в файле docker-compose
RHVOICE_SERVICE_PORT = '8080'  # порт, на котором запущен сервис RHVoice
RHVOICE_ORATOR_NAME = 'artemiy'  # Literal["aleksandr", "anna", "arina", "artemiy", "elena", "irina", "pavel"]
RHVOICE_ORATOR_RATE = 30
RHVOICE_ORATOR_PITCH = 42
RHVOICE_ORATOR_VOLUME = 100
# ==========================

# ===== Annoy Config =====
ANNOY_N_TREES = 256  # Количество деревьев в лесу Annoy (желательно степень двойки)
ANNOY_FILE_PATH = f'{ANNOY_MODEL_DIR}/annoy_trees.ann'  # Путь к файлу Annoy. Тут хранятся построенные леса
ANNOY_METRICS_NAME = 'euclidean'  # Метрика близости Annoy. "angular", "euclidean", "manhattan", "hamming", "dot"
# ========================

# ===== Scripts =====
DOWNLOAD_MODELS_SCRIPT = 'scripts/download_models.py'
# ===================

# ===== Download Model Link Config =====
DOWNLOAD_MODEL_LINK_NAVEC = f'https://storage.yandexcloud.net/natasha-navec/packs/{NAVEC_MODEL}'
DOWNLOAD_MODEL_LINK_VOSK = f'https://alphacephei.com/vosk/models/{VOSK_MODEL}.zip'
# ======================================
