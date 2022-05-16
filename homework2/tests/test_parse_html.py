import pytest

from weather.parse_html import get_html, get_weather_for_city, parse


@pytest.fixture()
def requests_mock(mocker):
    return mocker.patch('requests.get')


def test_get_weather_for_city():
    temperature = get_weather_for_city('<div id="weather-now-'
                                       'number">-9<span>°</span>')
    assert temperature == '-9°'


def test_get_html(requests_mock):
    requests_mock.return_value.text.return_value = "<!DOCTYPE html>"
    response = get_html("https://world-weather.ru/pogoda/russia/moscow")
    assert response.text() == "<!DOCTYPE html>"


def test_parse(requests_mock):
    requests_mock.return_value.text.return_value = "<!DOCTYPE html>"
    response = parse('mascow')
    assert response == "Error"
