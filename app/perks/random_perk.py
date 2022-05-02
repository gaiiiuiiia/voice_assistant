from typing import Dict
import random

from app.core.perk_base import PerkBase


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

    def random_coin(self, *args, **kwargs) -> str:
        choices = ['орёл', 'решка']

        return random.choice(choices)

