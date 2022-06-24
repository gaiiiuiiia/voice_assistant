import random
from typing import Dict
from typing import Optional

from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString


class GreetingsPerk(PerkBase):

    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'GreetingsPerk',
            'methods': {
                'greetings': {
                    'description': 'поприветствовать пользователя',
                    'keywords': ['привет', 'здравствуй', 'как дела', 'что нового'],
                    'args': [''],
                },
            },
        }

    def greetings(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        values = {
            'hello': 'привет',
            'very': 'очень',
            'glad': 'рад',
            'see': 'видеть',
        }
        variants = [
            '%hello% как дела',
            '%hello%',
            '%hello% %very% %glad% тебя %see%',
        ]

        return TemplateFormatString(random.choice(variants), values)
