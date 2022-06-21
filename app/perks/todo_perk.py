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

    def delete(self) -> None:
        pass


class TodoFileHandler:

    TODO_FILE_NAME = 'todos.txt'

    def __init__(self) -> None:
        self._prepare_todo_folder()
        logger.info(f'Файл заметок: %s' % self._get_todo_file_path())

    def save(self, todo: str) -> None:
        todo_file_path = self._get_todo_file_path()
        with open(todo_file_path, mode='a', encoding='utf-8') as file:
            file.write(todo + '\n')
        logger.info(f'Записано todo "%s"' % todo)

    def delete(self) -> None:
        todo_file_path = self._get_todo_file_path()
        os.remove(todo_file_path)

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

    def __init__(self) -> None:
        super().__init__()
        self._todo_file_handler = TodoFileHandler()

    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'TodoPerk',
            'methods': {
                'create_todo': {
                    'keywords': ['создай заметку', 'запиши на память', 'создать заметку'],
                    'args': [''],
                },
                'delete_todo': {
                    'keywords': ['удали заметки'],
                    'args': [''],
                },
            },
        }

    def create_todo(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        try:
            if args and type(args[0]) is str:
                self._todo_file_handler.save(args[0])
            else:
                self._process_listening()
        except Exception:
            logger.exception(f'Не удалось создать заметку')
            return TemplateFormatString(f'не удалось создать заметку')

        return TemplateFormatString(
            f'готово. заметка %success% создана',
            {'success': 'успешно'}
        )

    def delete_todo(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        try:
            self._todo_file_handler.delete()
        except Exception:
            logger.exception(f'Не удалось удалить заметки')
            return TemplateFormatString(f'Не удалось удалить заметки')

        return TemplateFormatString(
            f'Заметки были %success% удалены',
            {'success': 'успешно'}
        )

    def _process_listening(self) -> None:
        voice_recorder = VoiceRecorder()

        while True:
            query = voice_recorder.record()

            if query in self.STOP_WORDS:
                return

            self._todo_file_handler.save(query)
