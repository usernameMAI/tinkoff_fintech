import pytest

from app.database import Film
from app.keys import key_date, key_rating


@pytest.fixture()
def film():
    return Film(
        title="film",
        year_release=2000,
        month_release=5,
        rating=0,
        count_rating=0,
        count_review=0,
    )


def test_key_rating(film):
    assert key_rating(film) == 0.0
    film.average_rating = 5
    assert key_rating(film) == 5


def test_key_date(film):
    assert key_date(film) == (film.year_release * 12 + film.month_release)
