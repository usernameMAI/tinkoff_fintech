from http import HTTPStatus

from fastapi.testclient import TestClient

from app.db.models import User


def test_register(client: TestClient, db) -> None:
    login = 'test_login'
    data = {'login': login, 'password': 'test_password'}
    response = client.post('/register', json=data)
    user = db.query(User).filter_by(name=login).first()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'login': user.name}


def test_register_with_user_in_db(client: TestClient, first_user, db) -> None:
    data = {'login': first_user.name, 'password': 'test_password'}
    response = client.post('/register', json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_give_admin(client: TestClient, first_user, third_user_admin) -> None:
    user_id = first_user.id
    data = {'user_id': user_id}
    response = client.put(
        f'/admin/{user_id}',
        json=data,
        headers={'Authorization': f'Bearer {third_user_admin.name}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': user_id, 'status': 'successfully'}


def test_give_admin_without_user_ib_db(
    client: TestClient, first_user, third_user_admin
) -> None:
    user_id = first_user.id
    data = {'user_id': user_id}
    response = client.put(
        f'/admin/{0}',
        json=data,
        headers={'Authorization': f'Bearer {third_user_admin.name}'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_give_admin_without_rights(
    client: TestClient, first_user, third_user_admin
) -> None:
    user_id = first_user.id
    data = {'user_id': user_id}
    response = client.put(
        f'/admin/{first_user.id}',
        json=data,
        headers={'Authorization': f'Bearer {first_user.name}'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
