from http import HTTPStatus

from fastapi.testclient import TestClient

from app.db.models import Like, Post, User, UserRating


def test_rate_post(client: TestClient, first_post: Post, first_user: User, db) -> None:
    data = {'post_id': first_post.id, 'grade': True}
    response = client.put(
        f'/post/{first_post.id}/rate?grade=true',
        data=data,
        headers={'Authorization': f'Bearer {first_user.name}'},
    )
    rating = db.query(Like).filter_by(author=first_user, post=first_post).first()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'post_id': first_post.id,
        'rating': UserRating.LIKE,
        'status': 'successfully',
    }
    assert rating.rating == UserRating.LIKE
    #   если оценка уже стоит
    response = client.put(
        f'/post/{first_post.id}/rate?grade=true',
        data=data,
        headers={'Authorization': f'Bearer {first_user.name}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'post_id': first_post.id,
        'rating': UserRating.LIKE,
        'status': 'successfully',
    }
    assert rating.rating == UserRating.LIKE


def test_rate_post_without_post(client: TestClient, first_user) -> None:
    post_id = 0
    data = {'post_id': post_id, 'grade': True}
    response = client.put(
        f'/post/{post_id}/rate?grade=true',
        data=data,
        headers={'Authorization': f'Bearer {first_user.name}'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
