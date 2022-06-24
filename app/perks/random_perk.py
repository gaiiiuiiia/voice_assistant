import random
from typing import Dict
from typing import Optional

from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString


class RandomPerk(PerkBase):
    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'RandomPerk',
            'methods': {
                'random_coin': {
                    'description': 'подбросить монету',
                    'keywords': ['подбрось монетку', 'подбрось монету', 'кинь монетку', 'кинь монету'],
                    'args': [''],
                },
            },
        }

    def random_coin(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        side = random.choice(['орёл', 'решка'])
        values = {
            'toss': 'подкинул',
            'coin': 'монету',
            'drop': 'выпадает',
            'luck': 'повезло',
        }

        variants = [
            f'%toss% %coin% и %drop% {side}',
            f'тебе %drop% {side}',
            f'{side}',
            f'тебе %luck% %drop% {side}',
        ]

        return TemplateFormatString(random.choice(variants), values)

