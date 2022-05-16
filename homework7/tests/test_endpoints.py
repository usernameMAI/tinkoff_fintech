from http import HTTPStatus

from fastapi.testclient import TestClient
from mock import patch

from app.endpoints import router
from tests.conftest import fake_redis

test_client = TestClient(router)


@patch('app.redis.r', fake_redis)
def test_last_messages_with():
    response = test_client.get('/last_messages')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'messages': ''}


def test_get():
    response = test_client.get('/')
    assert response.status_code == HTTPStatus.OK
