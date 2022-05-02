from typing import Dict

from app.core.perk_base import PerkBase


class WeatherPerk(PerkBase):

    def get_manifest(cls) -> Dict:
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
