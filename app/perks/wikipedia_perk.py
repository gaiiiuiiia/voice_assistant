import inspect
import logging
import random
from typing import Dict
from typing import Optional

import wikipedia as wiki

from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString

logger = logging.getLogger(__name__)


class WikipediaPerk(PerkBase):

    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'GreetingsPerk',
            'methods': {
                'wiki_search': {
                    'description': 'найти что-нибудь в википедии',
                    'keywords': ['что такое', 'кто такой', 'кто такая', 'определение', 'как ты думаешь'],
                    'args': [''],
                },
            },
        }

    def wiki_search(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        query = kwargs.get('query')

        if type(query) is not str:
            logger.warning(f'Аргумент должен быть строкой %s::%s, но был передан %s' % (
                self.__class__.__name__,
                inspect.currentframe().f_code.co_name,
                type(query),
            ))
            return

        if not query:
            return

        count_sentences = random.choice(range(2, 3))
        wiki.set_lang('ru')
        try:
            wiki_response = wiki.summary(query, sentences=count_sentences)
        except Exception:
            logger.exception('Ошибка при обработки вики запроса')
            return

        return TemplateFormatString(wiki_response)
