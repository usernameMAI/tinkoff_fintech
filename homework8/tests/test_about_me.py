from http import HTTPStatus
from typing import Dict

from fastapi.testclient import TestClient


def test_get_info_about_me(client: TestClient, first_user) -> None:
    data: Dict[None, None] = {}
    response = client.get(
        '/user/me', json=data, headers={'Authorization': 'Bearer login'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'login': 'login'}


def test_get_info_about_me_without_db(client: TestClient) -> None:
    data: Dict[None, None] = {}
    response = client.get(
        '/user/me', json=data, headers={'Authorization': 'Bearer login'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User does not exist'}
