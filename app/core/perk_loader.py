from typing import List
import logging
import os
import importlib

from app.core.perk_base import PerkBase
from app.core.perk_validator import PerkValidator

from app.exceptions.incorrect_perk_class_exception import IncorrectPerkClassException

logger = logging.getLogger(__name__)


class PerkLoader:
    """
    Отвечает за загрузку перков из директории
    """

    def __init__(self, perk_validator: PerkValidator, directory: str) -> None:
        self._directory = directory
        self._perk_validator = perk_validator

    def load(self) -> List[PerkBase]:
        """
        Возвращает список объектов перков.
        :return:
        """

        perks = self._load_perks()
        validated_perks = self._get_valid_perks(perks)

        return validated_perks

    def _load_perks(self) -> List[PerkBase]:
        perk_instances = []

        modules = os.listdir(self._directory)
        for module in modules:
            module_path = os.sep.join([self._directory, module.rsplit('.', 1)[0]])
            module_path = module_path.replace(os.sep, '.')

            class_name = self.__get_class_name_from_module_name(module)

            instance = self._runtime_module_import(module_path, class_name)()

            perk_instances.append(instance)

        return perk_instances

    def _get_valid_perks(self, perks: List[PerkBase]) -> List[PerkBase]:
        valid_perks = []

        for perk in perks:
            try:
                self._perk_validator.validate(perk)
            except IncorrectPerkClassException:
                continue

            valid_perks.append(perk)
            logger.info(f'Перк %s прошел валидацию' % str(perk))

        return valid_perks

    @staticmethod
    def _runtime_module_import(module_path: str, class_name: str) -> type(PerkBase):
        module = importlib.import_module(module_path)

        return getattr(module, class_name)

    @staticmethod
    def __get_class_name_from_module_name(file_name: str) -> str:
        file_name_without_ext = file_name.split('.')[0]
        components = file_name_without_ext.split('_')
        return ''.join(map(str.capitalize, components))
