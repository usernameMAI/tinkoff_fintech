# pylint: disable=R0913
from http import HTTPStatus

from fastapi.testclient import TestClient

from app.config import settings
from app.db.models import Post


def test_add_post(client: TestClient, first_user, post_data, db) -> None:
    response = client.post(
        '/post', data=post_data, headers={'Authorization': 'Bearer login'}
    )
    assert response.status_code == HTTPStatus.OK
    post = db.query(Post).filter_by(header=post_data['header']).first()
    assert post.header == post_data['header']
    assert post.text == post_data['text']


def test_add_post_with_post_in_db(
    client: TestClient, first_user, first_post, post_data, db
) -> None:
    response = client.post(
        '/post', data=post_data, headers={'Authorization': 'Bearer login'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Post already exist'}


def test_delete_post_by_id(
    client: TestClient,
    first_user,
    first_post,
    first_comment_on_first_posts_first_user,
    first_like_on_first_posts_first_user,
    db,
) -> None:
    post_id = first_post.id
    data = {'post_id': post_id}
    response = client.delete(
        f'/post/{post_id}/delete', data=data, headers={'Authorization': 'Bearer login'}
    )
    first_post = db.query(Post).filter_by(id=post_id).first()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': post_id, 'status': 'successfully'}
    assert first_post is None


def test_delete_post_by_id_without_post_in_db(client: TestClient) -> None:
    post_id = -1
    data = {'post_id': post_id}
    response = client.delete(
        f'/post/{post_id}/delete', data=data, headers={'Authorization': 'Bearer login'}
    )
    assert response.json() == {'detail': 'Post does not exist'}


def test_delete_post_by_id_without_rights(
    client: TestClient, first_post, second_user
) -> None:
    post_id = first_post.id
    data = {'post_id': post_id}
    response = client.delete(
        f'/post/{post_id}/delete', data=data, headers={'Authorization': 'Bearer login2'}
    )
    assert response.json() == {'detail': 'You are not an author or an admin'}


def test_get_post_by_id(client: TestClient, first_user, first_post, db) -> None:
    data = {'post_id': first_post.id}
    response = client.get(f'/post/{first_post.id}', json=data)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == first_post.id


def test_get_post_by_id_without_post_in_db(client: TestClient, db) -> None:
    post_id = 1
    data = {'post_id': post_id}
    response = client.get(f'/post/{post_id}', json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Post does not exist'}


def test_get_user_posts(client: TestClient, first_user, first_post) -> None:
    data = {'user_id': first_user.id}
    response = client.get(
        f'/user/1/post?posts_per_page={settings.DEFAULT_POSTS_PER_PAGE}&page={settings.START_PAGE}',
        json=data,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]['id'] == first_post.id


def test_get_user_posts_without_posts(client: TestClient) -> None:
    data = {'user_id': 0}
    response = client.get(
        f'/user/1/post?posts_per_page={settings.DEFAULT_POSTS_PER_PAGE}&page={settings.START_PAGE}',
        json=data,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_get_last_day_posts(client: TestClient, first_post) -> None:
    response = client.get(
        f'/posts/last_day?posts_per_page='
        f'{settings.DEFAULT_POSTS_PER_PAGE}&page={settings.START_PAGE}',
        json={},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]['id'] == first_post.id
