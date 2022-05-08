from typing import Dict
import random

from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString


class RandomPerk(PerkBase):
    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'RandomPerk',
            'methods': {
                'random_coin': {
                    'keywords': ['подбрось монетку', 'подбрось монету', 'кинь монетку', 'кинь монету'],
                    'args': [''],
                },
            },
        }

    def random_coin(self, *args, **kwargs) -> TemplateFormatString:
        values = {
            'side': random.choice(['орёл', 'решка']),
        }

        variants = [
            'подкинул монету и выпал %side%',
            'выпал %side%',
            '%side%',
            'повезло выпал %side%',
        ]

        return TemplateFormatString(random.choice(variants), values)

