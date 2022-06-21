from typing import Dict
from typing import Optional
from typing import Protocol

import logging
import os

from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString
from app.core.voice_recorder import VoiceRecorder
from app.lib.lib import recursively_create_folders

import app.config as config

logger = logging.getLogger(__name__)


class TodoHandler(Protocol):
    def save(self, todo: str) -> None:
        pass


class TodoFileHandler:

    TODO_FILE_NAME = 'todos.txt'

    def __init__(self) -> None:
        self._prepare_todo_folder()

    def save(self, todo: str) -> None:
        file_to_save = self._get_todo_file_path()
        with open(file_to_save, mode='a', encoding='utf-8') as file:
            file.write(todo + '\n')
        logger.info(f'Записано todo "%s"' % todo)

    def _prepare_todo_folder(self) -> None:
        todo_folder_path = self._get_todo_folder_path()
        if not os.path.exists(todo_folder_path):
            recursively_create_folders(todo_folder_path)

    def _get_todo_file_path(self) -> str:
        return os.sep.join([config.get_path_os_sep(config.ASSETS_DIR), self.TODO_FILE_NAME])

    def _get_todo_folder_path(self) -> str:
        split_path = self._get_todo_file_path().split(os.sep)
        split_path.pop()

        return os.sep.join(split_path)


class TodoPerk(PerkBase):

    # Слова, которые завершают запись заметок
    STOP_WORDS = {'готово', 'хватит', 'завершить', 'конец'}

    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'TodoPerk',
            'methods': {
                'create_todo': {
                    'keywords': ['создай заметку', 'запиши на память'],
                    'args': [''],
                },
            },
        }

    def create_todo(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        todo_file_handler = TodoFileHandler()

        try:
            if args and type(args[0]) is str:
                todo_file_handler.save(args[0])
            else:
                self._process_listening(todo_file_handler)
        except Exception:
            logger.exception(f'Не удалось создать заметку')
            return TemplateFormatString(f'не удалось создать заметку')

        return TemplateFormatString(f'готово. заметка %was_created%', {'was_created': 'создана'})

    def _process_listening(self, todo_handler: TodoHandler) -> None:
        voice_recorder = VoiceRecorder()

        while True:
            query = voice_recorder.record()

            if query in self.STOP_WORDS:
                return

            todo_handler.save(query)
