import logging
from typing import Dict
from typing import List
from typing import Optional

import random
from copy import deepcopy

from app.core.perk_base import PerkBase
from app.core.perk_manager import PerkManager
from app.core.template_format_string import TemplateFormatString
from app.exceptions.incorrect_perk_class_exception import IncorrectPerkClassException

logger = logging.getLogger(__name__)


class CandoPerk(PerkBase):
    """
    Can Do Perk
    """

    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'CandoPerk',
            'methods': {
                'cando': {
                    'description': 'рассказать о собственных навыках',
                    'keywords': ['расскажи о себе', 'что ты умеешь', 'твои навыки'],
                    'args': [''],
                },
            },
        }

    def cando(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        perk_manager: PerkManager = kwargs.get('perk_manager')

        if type(perk_manager) is not PerkManager:
            return

        example_string = self._get_example_string(perk_manager.get_loaded_perks())

        if random.random() > 0.5:
            return TemplateFormatString(f'я могу много чего :) %s' % example_string)

        all_perks_manifests = list(map(lambda perk: perk.get_manifest(), perk_manager.get_loaded_perks()))

        # список из описаний перков
        manifest_descriptions: List[..., List[str]] = list(map(
            lambda manifest: self.__get_manifest_descriptions(manifest),
            all_perks_manifests
        ))

        random.shuffle(manifest_descriptions)

        # строка, состоящая из описаний перков через запятую
        joined_descriptions = ', '.join(
            [', '.join(descriptions) for descriptions in manifest_descriptions if all(descriptions)]
        )

        return TemplateFormatString(f'я могу %s. %s' % (joined_descriptions, example_string))

    def _get_example_string(self, perks: List[PerkBase]) -> Optional[str]:
        """
        Получить строку, описывающую пример использования перка.
        :param perk:
        :return:
        """
        perks = deepcopy(perks)
        random.shuffle(perks)

        for perk in perks:
            example_string = self.__construct_example_string(perk)
            if example_string:
                return example_string

    @staticmethod
    def __construct_example_string(perk: PerkBase) -> Optional[str]:
        method_name = random.choice(perk.get_manifest_methods())
        if not method_name:
            return

        try:
            method_manifest = perk.get_method_manifest(method_name)
        except IncorrectPerkClassException:
            return

        description = method_manifest.get('description')
        keywords = method_manifest.get('keywords')

        if not description or not keywords:
            return

        return f'Например, чтобы %s, скажи мне "%s...".' % (description, random.choice(keywords))

    @staticmethod
    def __get_manifest_descriptions(manifest: Dict) -> List:
        """
        Получить список, состоящий из полей description перка.
        :param manifest:
        :return:
        List
        """
        methods = manifest.get('methods')

        if not methods:
            return []

        return [method.get('description') for method in methods.values()]
