from typing import Dict

from app.core.perk_base import PerkBase


class WeatherPerk(PerkBase):

    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'WeatherPerk',
            'methods': {
                'weather': {
                    'keywords': ['погода', 'температура на улице'],
                    'args': [''],
                },
            },
        }

    def weather(self) -> None:
        pass
