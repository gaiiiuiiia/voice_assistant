from typing import Dict

from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString


class GreetingsPerk(PerkBase):

    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'GreetingsPerk',
            'methods': {
                'greetings': {
                    'keywords': ['привет', 'как дела', 'что нового'],
                    'args': [''],
                },
            },
        }

    def greetings(self, *args, **kwargs) -> TemplateFormatString:
        return TemplateFormatString('Привет, Максим! Как твои дела?')
