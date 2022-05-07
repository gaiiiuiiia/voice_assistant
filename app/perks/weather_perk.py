from typing import Dict

from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString


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

    def weather(self, *args, **kwargs) -> TemplateFormatString:
        pass
