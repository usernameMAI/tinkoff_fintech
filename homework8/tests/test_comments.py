from http import HTTPStatus
from typing import Dict

from fastapi.testclient import TestClient

from app.config import settings
from app.db.models import Comment, Post, User


def test_add_comment(client: TestClient, first_user, first_post, db) -> None:
    text = 'test text'
    data = {'post_id': first_post.id, 'text': text}
    response = client.post(
        f'/post/{first_post.id}/comment',
        json=data,
        headers={'Authorization': f'Bearer {first_user.name}'},
    )
    assert response.status_code == HTTPStatus.OK
    comment = db.query(Comment).filter_by(author=first_user, post=first_post).first()
    assert comment.text == text


def test_add_comment_without_post(client: TestClient, first_user) -> None:
    text = 'test text'
    post_id = 0
    data = {'post_id': post_id, 'text': text}
    response = client.post(
        f'/post/{post_id}/comment',
        json=data,
        headers={'Authorization': f'Bearer {first_user.name}'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_comment(
    client: TestClient,
    first_user: User,
    first_post: Post,
    first_comment_on_first_posts_first_user: Comment,
    db,
) -> None:
    data = {
        'post_id': first_post.id,
        'comment_id': first_comment_on_first_posts_first_user.id,
    }
    response = client.delete(
        f'post/{first_post.id}/comment/{first_comment_on_first_posts_first_user.id}',
        json=data,
        headers={'Authorization': f'Bearer {first_user.name}'},
    )
    assert response.status_code == HTTPStatus.OK
    comment = db.query(Comment).filter_by(author=first_user, post=first_post).first()
    assert comment is None


def test_delete_comment_without_comment_in_db(
    client: TestClient, first_user: User, first_post: Post, db
) -> None:
    comment_id = 0
    data = {'post_id': first_post.id, 'comment_id': comment_id}
    response = client.delete(
        f'post/{first_post.id}/comment/{comment_id}',
        json=data,
        headers={'Authorization': f'Bearer {first_user.name}'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_comment_without_rights(
    client: TestClient,
    second_user: User,
    first_post: Post,
    first_comment_on_first_posts_first_user: Comment,
    db,
) -> None:
    comment_id = first_comment_on_first_posts_first_user.id
    data = {'post_id': first_post.id, 'comment_id': comment_id}
    response = client.delete(
        f'post/{first_post.id}/comment/{comment_id}',
        json=data,
        headers={'Authorization': f'Bearer {second_user.name}'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_comments(
    client: TestClient, first_user, first_post, first_comment_on_first_posts_first_user
) -> None:
    data: Dict[None, None] = {}
    response = client.get(
        f'post/{first_post.id}/comments?posts_per_page='
        f'{settings.DEFAULT_POSTS_PER_PAGE}&page={settings.START_PAGE}',
        json=data,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0] == {
        'id': first_comment_on_first_posts_first_user.id,
        'author_id': first_user.id,
        'text': first_comment_on_first_posts_first_user.text,
    }
