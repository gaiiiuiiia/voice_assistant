import unittest

from app.perks.weather_perk import WeatherPerk


class TestWeatherPerk(unittest.TestCase):

    def test_weather(self) -> None:
        weather_perk = WeatherPerk()

        result = weather_perk.weather(query='яблоко и вишня')

