# pylint: disable=E1101
import pytest
from fastapi.testclient import TestClient
from mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from app.db.base import Base
from app.db.init_db import init_db
from app.db.models import Comment, Like, Post, User, UserRating, UserRole
from app.db.session import create_session

test_engine = create_engine('sqlite:///test_data.db')
Session = sessionmaker(bind=test_engine)


@pytest.fixture(scope='session')
def client():
    test_client = TestClient(app.app)  # type: ignore[attr-defined]
    return test_client


@pytest.fixture(autouse=True)
def _init_db():
    Base.metadata.create_all(bind=test_engine)  # type: ignore[attr-defined]

    with patch('app.db.session.get_engine') as mock:
        with patch('app.db.init_db.load_admins') as load_admins_mock:
            load_admins_mock.return_value = None
            mock.return_value = test_engine
            with create_session() as session:
                init_db(session)
                yield session

    Base.metadata.drop_all(bind=test_engine)  # type: ignore[attr-defined]


@pytest.fixture()
def db(_init_db):
    return _init_db


@pytest.fixture()
def first_user(db) -> User:
    user = User(name='login', password='1234')  # type: ignore[call-arg]
    db.add(user)
    db.commit()
    return user


@pytest.fixture()
def second_user(db) -> User:
    user = User(name='login2', password='1234')  # type: ignore[call-arg]
    db.add(user)
    db.commit()
    return user


@pytest.fixture()
def third_user_admin(db) -> User:
    user = User(name='login3', password='1234', role=UserRole.ADMIN)  # type: ignore[call-arg]
    db.add(user)
    db.commit()
    return user


@pytest.fixture()
def first_post(db, first_user) -> Post:
    post = Post(header='test header', text='test text', author=first_user)  # type: ignore[call-arg]
    db.add(post)
    db.commit()
    return post


@pytest.fixture()
def second_post(db, first_user) -> Post:
    post = Post(
        header='test header2', text='test text2', author=first_user
    )  # type: ignore[call-arg]
    db.add(post)
    db.commit()
    return post


@pytest.fixture()
def post_data():
    header = 'test header'
    text = 'test text'
    data = {'header': header, 'text': text}
    return data


@pytest.fixture()
def first_comment_on_first_posts_first_user(db, first_post, first_user) -> Comment:
    comment = Comment(
        text='test comment', author=first_user, post=first_post
    )  # type: ignore[call-arg]
    db.add(comment)
    db.commit()
    return comment


@pytest.fixture()
def first_like_on_first_posts_first_user(db, first_post, first_user) -> Like:
    like = Like(
        rating=UserRating.LIKE, author=first_user, post=first_post
    )  # type: ignore[call-arg]
    db.add(like)
    db.commit()
    return like


@pytest.fixture()
def my_list():
    return [1, 2, 3, 4, 5]
