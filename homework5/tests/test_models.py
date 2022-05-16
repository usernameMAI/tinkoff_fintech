import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models import NewFilm, NewUser


def test_new_user():
    new_user = NewUser(name="test", password="test")
    assert new_user.name == "test"
    assert new_user.password == "test"


def test_new_user_with_empty_login():
    with pytest.raises(HTTPException):
        NewUser(name="", password="test")


def test_new_user_with_empty_password():
    with pytest.raises(HTTPException):
        NewUser(name="test", password="")


def test_new_user_with_long_name():
    with pytest.raises(HTTPException):
        NewUser(name="12345123451234512345", password="test")


def test_new_user_with_long_password():
    with pytest.raises(HTTPException):
        NewUser(name="test", password="12345123451234512345")


def test_new_film():
    new_film = NewFilm(title="test", year=2020, month=10)
    assert new_film.title == "test"
    assert new_film.year == 2020
    assert new_film.month == 10


def test_new_film_with_empty_title():
    with pytest.raises(HTTPException):
        NewFilm(title="", year=2020, month=10)


def test_new_film_with_long_title():
    with pytest.raises(HTTPException):
        NewFilm(title="12345123456123456123456", year=2020, month=10)


def test_new_film_with_none_year():
    with pytest.raises(ValidationError):
        NewFilm(title="test", year=None, month=10)


def test_new_film_with_negative_year():
    with pytest.raises(HTTPException):
        NewFilm(title="test", year=-10, month=10)


def test_new_film_with_none_month():
    with pytest.raises(ValidationError):
        NewFilm(title="test", year=10, month=None)


def test_new_film_with_zero_month():
    with pytest.raises(HTTPException):
        NewFilm(title="test", year=10, month=0)


def test_new_film_with_negative_month():
    with pytest.raises(HTTPException):
        NewFilm(title="test", year=10, month=-10)


def test_new_film_with_big_month():
    with pytest.raises(HTTPException):
        NewFilm(title="test", year=10, month=20)
