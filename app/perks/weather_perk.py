import inspect
import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeAlias

import requests
from natasha import LocationExtractor
from yargy.parser import Match

import app.config as config
from app.core.perk_base import PerkBase
from app.core.template_format_string import TemplateFormatString
from app.exceptions.api_service_exception import ApiServiceException

logger = logging.getLogger(__name__)

Celsius: TypeAlias = int


class WeatherType(str, Enum):
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморось'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    CLEAR = 'Ясно'
    FOG = 'Туман'
    CLOUDS = 'Облачно'


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    city: str


def parse_locations_from_string(text: str) -> List[str]:
    extractor = LocationExtractor()
    matches: List[Match] = extractor(text)

    return [match.fact.name for match in matches]


class OpenWeatherHandler:
    URL = 'http://api.openweathermap.org/data/2.5/weather'

    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key

    def get_weather(self, location: str) -> Weather:
        url = f'{self.URL}?appid={self.__api_key}&q={location}&lang=ru&units=metric'
        openweather_dict = requests.get(url).json()

        return Weather(
            temperature=self.__parse_temperature(openweather_dict),
            weather_type=self.__parse_weather_type(openweather_dict),
            city=self.__parse_city(openweather_dict)
        )

    @staticmethod
    def __parse_temperature(openweather_dict: dict) -> Celsius:
        return round(openweather_dict['main']['temp'])

    @staticmethod
    def __parse_weather_type(openweather_dict: dict) -> WeatherType:
        try:
            weather_type_id = str(openweather_dict['weather'][0]['id'])
        except (IndexError, KeyError):
            raise ApiServiceException

        weather_types = {
            '1': WeatherType.THUNDERSTORM,
            '2': WeatherType.DRIZZLE,
            '3': WeatherType.RAIN,
            '5': WeatherType.SNOW,
            '6': WeatherType.FOG,
            '800': WeatherType.CLEAR,
            '80': WeatherType.CLOUDS,
        }

        for _id, _weather_type in weather_types.items():
            if weather_type_id.startswith(_id):
                return _weather_type

        raise ApiServiceException

    @staticmethod
    def __parse_city(openweather_dict: dict) -> str:
        return openweather_dict['name']


class WeatherPerk(PerkBase):

    def _do_create_manifest(self) -> Dict:
        return {
            'name': 'WeatherPerk',
            'methods': {
                'weather': {
                    'description': 'узнать, какая сейчас погода',
                    'keywords': ['погода', 'температура на улице'],
                    'args': [''],
                },
            },
        }

    def weather(self, *args, **kwargs) -> Optional[TemplateFormatString]:
        query = kwargs.get('query') \
            if type(kwargs.get('query')) is str \
            else config.DEFAULT_WEATHER_LOCATION

        if type(query) is not str:
            logger.warning(f'Аргумент должен быть строкой %s::%s, но был передан %s' % (
                self.__class__.__name__,
                inspect.currentframe().f_code.co_name,
                type(query),
            ))
            return

        api_key = os.getenv('OPENWEATHER_API_KEY')

        if not api_key:
            raise RuntimeError(f'%s. Не удалось определить OPENWEATHER_API_KEY' % self.__class__.__name__)

        parsed_locations = parse_locations_from_string(query)

        if not parsed_locations:
            logger.info(f'Поиск погоды не удался. Так как не удалось определить локацию из запроса %s' % query)
            return

        location = parsed_locations[0]

        weather_handler = OpenWeatherHandler(api_key)
        weather = weather_handler.get_weather(location)

        return TemplateFormatString(
            f'сейчас в {weather.city} {weather.weather_type}. %feels% как {weather.temperature} градус Цельсия.',
            {'feels': 'ощущается'}
        )
