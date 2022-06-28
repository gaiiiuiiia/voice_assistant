import logging
import os
import random
from typing import Dict
from typing import List
from typing import Optional
from typing import Protocol

import app.config as config
from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString
from app.core.voice_recorder import VoiceRecorder
from app.exceptions.todo_file_exception import TodoFileException
from app.exceptions.todo_not_exist_exception import TodoNotExistException
from app.lib.lib import recursively_create_folders

logger = logging.getLogger(__name__)


class TodoHandler(Protocol):
    def save(self, todo: str) -> None:
        pass

    def delete(self) -> None:
        pass

    def read(self) -> List[str]:
        pass

    def delete_particular_todo(self, todo: str) -> None:
        pass


class TodoFileHandler:

    TODO_FILE_NAME = 'todos.txt'

    def __init__(self) -> None:
        self._prepare_todo()

    def save(self, todo: str) -> None:
        todo_file_path = self._get_todo_file_path()
        try:
            with open(todo_file_path, mode='a', encoding='utf-8') as file:
                file.write(todo + '\n')
                logger.info(f'Записано todo "%s"' % todo)
        except OSError:
            raise TodoFileException('Не удалось сохранить заметку "%s"' % todo)

    def delete(self) -> None:
        todo_file_path = self._get_todo_file_path()
        try:
            with open(todo_file_path, mode='w', encoding='utf-8'):
                logger.info('Заметки были стерты')
        except OSError:
            raise TodoFileException('Не удалось стереть заметки')

    def read(self) -> List[str]:
        todo_file_path = self._get_todo_file_path()
        try:
            with open(todo_file_path, mode='r', encoding='utf-8') as file:
                return file.readlines()
        except OSError:
            raise TodoFileException('Не удалось открыть файл заметок')

    def delete_particular_todo(self, todo: str) -> None:
        created_todo_list = self.read()
        strip_todo = todo.strip()
        filtered_todos = list(filter(lambda t: strip_todo not in t, created_todo_list))

        if len(created_todo_list) == len(filtered_todos):
            raise TodoNotExistException

        self.delete()
        for t in filtered_todos:
            self.save(t)
            print(t)

    def _prepare_todo(self) -> None:
        todo_folder_path = self._get_todo_folder_path()
        if not os.path.exists(todo_folder_path):
            recursively_create_folders(todo_folder_path)

        todo_file_path = self._get_todo_file_path()
        if not os.path.exists(todo_file_path):
            with open(todo_file_path, mode='w', encoding='utf-8'):
                logger.info(f'Создан файл заметок: %s' % self._get_todo_file_path())

    def _get_todo_file_path(self) -> str:
        return os.sep.join([self._get_todo_folder_path(), self.TODO_FILE_NAME])

    @staticmethod
    def _get_todo_folder_path() -> str:
        return config.get_path_os_sep(config.ASSETS_DIR)


class TodoPerk(PerkBase):

    # Слова, которые завершают запись заметок
    STOP_WORDS = {'готово', 'хватит', 'завершить', 'конец'}

    def __init__(self) -> None:
        super().__init__()
        self._todo_file_handler: TodoHandler = TodoFileHandler()

    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'TodoPerk',
            'methods': {
                'create_todo': {
                    'description': 'создать заметки',
                    'keywords': ['создай заметку', 'создай заметки', 'запиши на память',
                                 'создать заметку', 'заметка', 'запиши заметку'],
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
                'delete_particular_todo': {
                    'description': 'удалить заметку по шаблону',
                    'keywords': ['удали заметку'],
                    'args': [''],
                },
            },
        }

    def create_todo(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        query = kwargs.get('query')

        try:
            if type(query) is str and query:
                self._todo_file_handler.save(query)
                print(query)
            else:
                self._process_listening()
        except TodoFileException:
            return TemplateFormatString('не удалось создать заметку')

        return TemplateFormatString('готово. заметка %success% создана', {'success': 'успешно'})

    def delete_todo(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        try:
            self._todo_file_handler.delete()
        except TodoFileException:
            return TemplateFormatString('Не удалось удалить заметки')

        if not len(self._todo_file_handler.read()):
            return TemplateFormatString(random.choice([
                'заметки были пусты',
                'заметок не было',
                'заметок нет',
            ]))

        return TemplateFormatString('Заметки были %success% удалены', {'success': 'успешно'})

    def read_todo(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        try:
            todos = self._todo_file_handler.read()
        except TodoFileException:
            return TemplateFormatString('не удалось прочитать твои заметки')

        todos = map(str.strip, filter(lambda todo: len(todo.strip()) > 0, todos))
        result = ', '.join(todos)

        if not result:
            return TemplateFormatString(random.choice([
                'у тебя в заметках пусто',
                'у тебя в заметках ничего не записано',
                'заметки пусты',
                'заметок нет',
            ]))

        return TemplateFormatString(f'у тебя в заметках %write% {result}', {'write': 'написано'})

    def delete_particular_todo(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        query = kwargs.get('query')

        if type(query) is str and query:
            try:
                self._todo_file_handler.delete_particular_todo(query)
            except TodoFileException:
                logger.exception('не удалось удалить заметку')
                return TemplateFormatString('не удалось удалить заметку')
            except TodoNotExistException:
                return TemplateFormatString('мы такую заметку не создавали')

        return TemplateFormatString('готово')

    def _process_listening(self) -> None:
        voice_recorder = VoiceRecorder()

        while True:
            query = voice_recorder.record()

            if query in self.STOP_WORDS:
                return

            self._todo_file_handler.save(query)
            print(query)
