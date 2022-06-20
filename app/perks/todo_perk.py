from typing import Dict
from typing import Optional

import logging
import os

from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString
from app.core.voice_recorder import VoiceRecorder
from app.lib.lib import recursively_create_folders

import app.config as config

logger = logging.getLogger(__name__)


class TodoFileHandler:

    TODO_FILE_NAME = 'todos.txt'

    def __init__(self) -> None:
        self._prepare_todo_folder()

    def write_todo(self, todo: str) -> bool:
        with open(self._get_todo_file_path(), mode='a', encoding='utf-8') as file:
            file.write(todo + '\n')
            logger.info(f'Записано todo "%s"' % todo)

        return True

    def _prepare_todo_folder(self) -> None:
        todo_folder_path = self._get_todo_folder_path()
        if not os.path.exists(todo_folder_path):
            recursively_create_folders(todo_folder_path)

        return

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

        try:
            query = args[0]
        except IndexError:
            self._process_listening()
            return TemplateFormatString(f'готово. заметки созданы')

        if type(query) is str:
            todo_file_handler = TodoFileHandler()
            todo_file_handler.write_todo(query)

    def _process_listening(self) -> None:
        voice_recorder = VoiceRecorder()
        todo_file_handler = TodoFileHandler()

        while True:
            query = voice_recorder.record()

            if query in self.STOP_WORDS:
                return

            todo_file_handler.write_todo(query)
