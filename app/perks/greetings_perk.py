from typing import Dict

from app.core.perk_base import PerkBase


class GreetingsPerk(PerkBase):

    def get_manifest(cls) -> Dict:
        return {
            'name': 'GreetingsPerk',
            'methods': {
                'greetings': {
                    'keywords': ['привет', 'как дела', 'что нового'],
                    'args': [''],
                },
            },
        }

    def greetings(self, *args, **kwargs) -> None:
        print('Привет, Максим! Как твои дела?')
