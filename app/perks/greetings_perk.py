from typing import Dict

import random

from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString


class GreetingsPerk(PerkBase):

    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'GreetingsPerk',
            'methods': {
                'greetings': {
                    'keywords': ['привет', 'здравствуй', 'как дела', 'что нового'],
                    'args': [''],
                },
            },
        }

    def greetings(self, *args, **kwargs) -> TemplateFormatString:
        values = {
            'hello': 'привет',
            'you': 'тебя',
        }
        variants = [
            # '%hello% как дела',
            # '%hello%',
            '%hello% очень рад %you% видеть',
        ]

        return TemplateFormatString(random.choice(variants), values)
