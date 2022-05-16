import pytest
from mock import patch

from weather.main_weather import main
from weather.parse_html import parse


def test_main_good():
    with patch('weather.parse_html.parse') as mock:
        mock.return_value = '-9°'
        assert main('moscow') is True
    with patch('weather.cache_weather.need_cache') as mock:
        mock.return_value = True
        parse('moscow')
    assert main('moscow') is True


def test_main_bad():
    assert main('mascow') is False
    with pytest.raises(AttributeError):
        parse(123)
