import logging

from app.core.perk_base import PerkBase
from app.exceptions.incorrect_perk_class_exception import IncorrectPerkClassException

logger = logging.getLogger(__name__)


class PerkValidator:

    # Используемые старт-слова в перках. Если в разных перков есть одинаковые старт-слова, валидатор выдаст исключение
    used_keywords = {}

    @classmethod
    def validate(cls, perk: PerkBase) -> None:
        cls._validate_perk_methods(perk)
        cls._validate_perk_keywords(perk)

    @staticmethod
    def _validate_perk_methods(perk: PerkBase) -> None:
        for method in perk.get_manifest_methods():
            if not getattr(perk, method, None):
                raise IncorrectPerkClassException(f'Перк %s не имеет метода %s, в то время как в манифесте он указан'
                                                  % (str(perk), method))

    @classmethod
    def _validate_perk_keywords(cls, perk: PerkBase) -> None:

        if str(perk) not in cls.used_keywords.keys():
            cls.used_keywords[str(perk)] = {}

        for method, keywords in perk.get_manifest_keywords().items():

            if method not in cls.used_keywords[str(perk)]:
                cls.used_keywords[str(perk)][method] = set()

            for keyword in keywords:
                try:
                    cls.__check_perk_keyword(perk, method, keyword)
                except IncorrectPerkClassException:
                    logger.info(f'Перк %s не будет включен в список активных перков' % str(perk))
                    cls.used_keywords.pop(str(perk))
                    raise

                cls.used_keywords[str(perk)][method].add(keyword)

    @classmethod
    def __check_perk_keyword(cls, perk: PerkBase, method: str, keyword: str) -> None:
        for used_perk, used_perk_methods in cls.used_keywords.items():
            for method_name, keywords in used_perk_methods.items():
                if keyword in keywords:
                    raise IncorrectPerkClassException(
                        f'Перк "%s" содержит ключевое слово "%s" метода "%s",'
                        f' которое уже используется перком "%s" в методе "%s"'
                        % (str(perk), keyword, method, used_perk, method_name)
                    )
