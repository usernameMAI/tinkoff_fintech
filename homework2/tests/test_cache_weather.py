import datetime

import pytest
from mock import patch

from weather.cache_weather import cache, need_cache


@pytest.fixture()
def file_mock(mocker):
    mock = mocker.MagicMock()
    return mock


def test_cache():
    def some_function(city):
        pass
    # Проверка, что декоратор возвращает функцию.
    assert callable(cache(some_function('some_city')))


def test_need_cache_time_exceed(file_mock):
    city = 'moscow'
    file_mock.get.return_value = True
    with patch('weather.cache_weather.get_datetime') as mock:
        mock.return_value = datetime.datetime.now() \
                            - datetime.timedelta(minutes=6)
        assert need_cache(file_mock, city) is True


def test_need_cache_not_file(file_mock):
    file_mock.get.return_value = None
    assert need_cache(file_mock, 'moscow') is True
