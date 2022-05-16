# pylint: disable=missing-module-docstring
from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

from weather.cache_weather import cache

URL = "https://world-weather.ru/pogoda/russia/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         ' "AppleWebKit/537.36 (HTML, like Gecko)'
                         ' Chrome/99.0.4844.51 Safari/537.36', 'accept': '*/*'}


def get_html(url: str, params=None):
    """
    Функция выполняет запрос к url.
    Возвращает html страницу.
    """
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_weather_for_city(html) -> str:
    """
    Функция парсит html и возвращает
    текущую температуру в градусах цельсия.
    """
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', id='weather-now-number')
    return items.get_text(strip=True)


@cache
def parse(city: str) -> str:
    """
    Функция получает текущую температуру в городе city.
    Если города city нет в России, либо он введён некорректно,
    то функция возвращает "Error".
    """
    html = get_html(f"{URL}{city}/")
    # Если код 200, то получилось сделать запрос.
    if html.status_code == HTTPStatus.OK:
        current_weather = get_weather_for_city(html.text)
        return current_weather
    error_message = "Error"
    return error_message
