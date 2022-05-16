import pytest
from fastapi.testclient import TestClient
from mock import patch

from app.app import app
from tests.test_functions import Base, Film, create_session, engine

client = TestClient(app)


@pytest.fixture(autouse=True)
def _init_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_register():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        data = {"name": "test", "password": "pass"}
        response = client.post("/register", json=data)
        assert response.status_code == 200
        assert response.json() == {"Status": "ok"}


def test_register_with_user_in_db():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        data = {"name": "test", "password": "pass"}
        client.post("/register", json=data)
        mock.return_value = create_session()
        response = client.post("/register", json=data)
        assert response.status_code == 400
        assert response.json() == {"detail": "User already registered"}


def test_add_film_without_auth():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        data = {"title": "test", "year": 2022, "month": 4}
        response = client.post("/add", json=data)
        assert response.status_code == 401


def test_add_film():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        data = {"title": "test", "year": 2022, "month": 4}
        response = client.post(
            "/add", json=data, headers={"Authorization": "Bearer login"}
        )
        assert response.status_code == 200
        assert response.json() == {"Status": "ok"}


def test_save_film_review_without_film_in_db():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        data = {
            "title": "test",
            "year": "1000",
            "month": "10",
            "new_review": "test_review",
        }
        response = client.post(
            "/review/string?year=2000&month=10&new_review=test_review",
            json=data,
            headers={"Authorization": "Bearer login"},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Film not exists"}


def test_save_film_review():
    with create_session() as session:
        film = Film(
            title="test_title",
            year_release=2022,
            month_release=4,
            rating=0,
            count_rating=0,
            count_review=0,
        )
        session.add(film)
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        data = {
            "title": "test_title",
            "year": "2022",
            "month": "4",
            "new_review": "test_review",
        }
        response = client.post(
            "/review/test_title?year=2022&month=4&new_review=test_review",
            json=data,
            headers={"Authorization": "Bearer login"},
        )
        assert response.status_code == 200
        assert response.json() == {"Status": "ok"}


def test_rate_film_without_film_in_db():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        data = {"title": "test_title", "year": "2022", "month": "4", "rating": 7}
        response = client.put(
            "/rate/test_title/7?year=2022&month=4",
            json=data,
            headers={"Authorization": "Bearer login"},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Film not exists"}


def test_rate_film():
    with create_session() as session:
        film = Film(
            title="test_title",
            year_release=2022,
            month_release=4,
            rating=0,
            count_rating=0,
            count_review=0,
        )
        session.add(film)
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        data = {"title": "test_title", "year": "2022", "month": "4", "rating": 7}
        response = client.put(
            "/rate/test_title/7?year=2022&month=4",
            json=data,
            headers={"Authorization": "Bearer login"},
        )
        assert response.status_code == 200
        assert response.json() == {"Status": "ok"}


def test_get_film():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        response = client.get(
            "/films?films_per_page=10&page=1", headers={"Authorization": "Bearer login"}
        )
        assert response.status_code == 200
        assert response.json() == {"Status": "ok"}


def test_films_top_rating():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        response = client.get(
            "/films/rating/top?films_per_page=10&page=1",
            headers={"Authorization": "Bearer login"},
        )
        assert response.status_code == 200
        assert response.json() == {"Status": "ok"}


def test_films_top_date():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        response = client.get(
            "/films/rating/date?films_per_page=10&page=1",
            headers={"Authorization": "Bearer login"},
        )
        assert response.status_code == 200
        assert response.json() == {"Status": "ok"}


def test_find_films_substring():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        response = client.get(
            "/films/substr?films_per_page=10&page=1",
            headers={"Authorization": "Bearer login"},
        )
        assert response.status_code == 200
        assert response.json() == {"Status": "ok"}


def test_about_film_without_film_in_db():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        response = client.get(
            "/about/test?year=2022&month=4", headers={"Authorization": "Bearer login"}
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Film not exists"}


def test_about_film_with_film_in_db():
    with create_session() as session:
        film = Film(
            title="test",
            year_release=2022,
            month_release=4,
            rating=0,
            count_rating=0,
            count_review=0,
        )
        session.add(film)
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        response = client.get(
            "/about/test?year=2022&month=4", headers={"Authorization": "Bearer login"}
        )
        assert response.status_code == 200
        assert response.json()["Status"] == "ok"


def test_film_reviews_without_film_in_db():
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        response = client.get(
            "/films/review/test?year=2022&month=4&films_per_page=10&page=1",
            headers={"Authorization": "Bearer login"},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Film not exists"}


def test_film_reviews_with_film_in_db():
    with create_session() as session:
        film = Film(
            title="test",
            year_release=2022,
            month_release=4,
            rating=0,
            count_rating=0,
            count_review=0,
        )
        session.add(film)
    with patch("app.app.create_session") as mock:
        mock.return_value = create_session()
        response = client.get(
            "/films/review/test?year=2022&month=4&films_per_page=10&page=1",
            headers={"Authorization": "Bearer login"},
        )
        assert response.status_code == 200
        assert response.json()["Status"] == "ok"
