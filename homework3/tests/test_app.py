from http import HTTPStatus

from mock import MagicMock

from app.todo import app, my_db
from app.database_class import save_title


def test_home_page():
    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == HTTPStatus.OK


def test_completed_page():
    with app.test_client() as test_client:
        response = test_client.get("/completed")
        assert response.status_code == HTTPStatus.OK


def test_active_page():
    with app.test_client() as test_client:
        response = test_client.get("/active")
        assert response.status_code == HTTPStatus.OK


def test_add_page():
    with app.test_client() as test_client:
        response = test_client.post("/add")
        assert response.status_code == HTTPStatus.FOUND


def test_update_page():
    with app.test_client() as test_client:
        logger = MagicMock()
        logger.debug.return_value = None
        save_title("Hello, world", my_db, logger)
        response_found = test_client.post("/update/1")
        response_not_found = test_client.post("/update/0")
        assert response_found.status_code == HTTPStatus.FOUND
        assert response_not_found.status_code == HTTPStatus.NOT_FOUND
