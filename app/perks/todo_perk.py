import logging
import os
from typing import Dict
from typing import List
from typing import Optional
from typing import Protocol

import app.config as config
from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString
from app.core.voice_recorder import VoiceRecorder
from app.lib.lib import recursively_create_folders

logger = logging.getLogger(__name__)


class TodoHandler(Protocol):
    def save(self, todo: str) -> None:
        pass

    def delete(self) -> None:
        pass

    def read(self) -> List[str]:
        pass


class TodoFileHandler:

    TODO_FILE_NAME = 'todos.txt'

    def __init__(self) -> None:
        self._prepare_todo()
        logger.info(f'Создан файл заметок: %s' % self._get_todo_file_path())

    def save(self, todo: str) -> None:
        todo_file_path = self._get_todo_file_path()
        with open(todo_file_path, mode='a', encoding='utf-8') as file:
            file.write(todo + '\n')
        logger.info(f'Записано todo "%s"' % todo)

    def delete(self) -> None:
        todo_file_path = self._get_todo_file_path()
        if os.path.exists(todo_file_path):
            os.remove(todo_file_path)

    def read(self) -> List[str]:
        todo_file_path = self._get_todo_file_path()

        with open(todo_file_path, mode='r', encoding='utf-8') as file:
            return file.readlines()

    def _prepare_todo(self) -> None:
        todo_folder_path = self._get_todo_folder_path()
        if not os.path.exists(todo_folder_path):
            recursively_create_folders(todo_folder_path)

        todo_file_path = self._get_todo_file_path()
        if not os.path.exists(todo_file_path):
            with open(todo_file_path, mode='w', encoding='utf-8'):
                pass

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
                    'description': 'создать заметки',
                    'keywords': ['создай заметку', 'создай заметки', 'запиши на память', 'создать заметку', 'заметка'],
                    'args': [''],
                },
                'delete_todo': {
                    'description': 'удалить заметки',
                    'keywords': ['удали заметки', 'удалить заметки'],
                    'args': [''],
                },
                'read_todo': {
                    'description': 'прочитать заметки',
                    'keywords': ['прочти заметки', 'прочитай заметки', 'заметки'],
                    'args': [''],
                },
            },
        }

    def create_todo(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        query = kwargs.get('query')

        try:
            if type(query) is str and query:
                self._todo_file_handler.save(query)
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

    def read_todo(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        todos = self._todo_file_handler.read()
        todos = map(str.strip, filter(lambda todo: len(todo.strip()) > 0, todos))
        result = ', '.join(todos)

        return TemplateFormatString(result)

    def _process_listening(self) -> None:
        voice_recorder = VoiceRecorder()

        while True:
            query = voice_recorder.record()

            if query in self.STOP_WORDS:
                return

            self._todo_file_handler.save(query)
