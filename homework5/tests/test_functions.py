from contextlib import contextmanager

import pytest
from mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from app.database import Base, Film, RateHistory, User
from app.functions import (
    authenticate_user,
    change_film_rating,
    convert_to_common_list,
    rating_correct,
)

engine = create_engine("sqlite:///test_data.db")
Session = sessionmaker(bind=engine)


@contextmanager
def create_session(**kwargs):
    """
    Функция создаёт сессию БД.
    """
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


@pytest.fixture(autouse=True)
def _init_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def film():
    return Film(
        title="test",
        year_release=2000,
        month_release=5,
        rating=0,
        count_rating=0,
        count_review=0,
    )


def test_authenticate_user():
    with patch("app.functions.create_session") as mock:
        mock.return_value = create_session()
        with create_session() as session:
            user = User(name="login", password=generate_password_hash("password"))
            session.add(user)
        assert authenticate_user("login", "password") is True


def test_authenticate_user_with_empty_db():
    with patch("app.functions.create_session") as mock:
        mock.return_value = create_session()
        assert authenticate_user("login", "password") is False


def test_rating_correct_too_big():
    assert rating_correct(100) is False


def test_rating_correct_zero():
    assert rating_correct(0) is False


def test_rating_correct_negative():
    assert rating_correct(-5) is False


def test_rating_correct():
    assert rating_correct(5) is True


def test_change_film_rating_without_film_in_rate_history(film):
    with create_session() as session:
        session.add(film)
    with create_session() as session:
        film = session.query(Film).filter_by(title="test").first()
        change_film_rating(film, 6, "user", session)
        assert film.rating == 6


def test_change_film_rating_with_film_in_rate_history():
    with create_session() as session:
        film = Film(
            title="test",
            year_release=2000,
            month_release=10,
            count_rating=1,
            count_review=0,
            rating=4,
            average_rating=4,
        )
        history = RateHistory(user_name="user", film_title="test", rating=4)
        session.add(film)
        session.add(history)
    with create_session() as session:
        film = session.query(Film).filter_by(title="test").first()
        change_film_rating(film, 6, "user", session)
        assert film.rating == 6


def test_convert_to_common_list(film):
    list_with_db_classes = [film]
    common_list = convert_to_common_list(list_with_db_classes)
    assert isinstance(common_list[0], dict)
