from contextlib import contextmanager
from http import HTTPStatus

import pytest
from mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application import app
from app.databases import Base, Cryptocurrency, OperationsHistory, PortfolioItem, User


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


def test_start_page():
    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == HTTPStatus.OK


def test_home_page():
    with app.test_client() as test_client:
        response = test_client.get("/home")
        assert response.status_code == HTTPStatus.FOUND


@patch("app.application.login", "Dmitriy")
def test_home_page_with_login():
    with app.test_client() as test_client:
        with create_session() as session:
            user = User(name="Dmitriy", money="1000")
            session.add(user)
        with patch("app.application.create_session") as mock:
            mock.return_value = create_session()
            response = test_client.get("/home")
            assert response.status_code == HTTPStatus.OK


@patch("app.application.login", "Dmitriy")
def test_history_page():
    with app.test_client() as test_client:
        with create_session() as session:
            user = User(name="Dmitriy", money="1000")
            operation = OperationsHistory(
                name_user="Dmitriy",
                name_crypto="Crypto1",
                cost="10",
                operation=False,
            )
            session.add(operation)
            session.add(user)
        with patch("app.application.create_session") as mock:
            mock.return_value = create_session()
            response = test_client.get("/history")
            assert response.status_code == HTTPStatus.OK


def test_portfolio_page():
    with app.test_client() as test_client:
        response = test_client.get("/portfolio")
        assert response.status_code == HTTPStatus.FOUND


@patch("app.application.login", "Dmitriy")
def test_portfolio_page_with_login():
    with app.test_client() as test_client:
        with patch("app.application.create_session"):
            response = test_client.get("/portfolio")
            assert response.status_code == HTTPStatus.OK


@patch("app.application.login", "Dmitriy")
def test_portfolio_sell_page():
    with app.test_client() as test_client:
        with patch("app.application.create_session") as mock:
            mock.return_value = create_session()
            with patch("app.functions.need_update_page") as update_mock:
                update_mock.return_value = False
                with create_session() as session:
                    user = User(name="Dmitriy", money="1000")
                    crypto = Cryptocurrency(id=1, name="Crypto1", price="100")
                    storage = PortfolioItem(
                        id=1, name_user="Dmitriy", name_crypto="Crypto1", count=1
                    )
                    session.add(user)
                    session.add(crypto)
                    session.add(storage)
                response = test_client.post("/portfolio/Crypto1")
                assert response.status_code == HTTPStatus.FOUND
                with create_session() as session:
                    money = session.query(User).filter_by(name="Dmitriy").first().money
                    assert money == "1100"


def test_buy_page():
    with app.test_client() as test_client:
        response = test_client.get("/buy")
        assert response.status_code == HTTPStatus.FOUND


@patch("app.application.login", "Dmitriy")
def test_buy_page_with_login():
    with app.test_client() as test_client:
        with patch("app.application.create_session") as _:
            response = test_client.get("/buy")
            assert response.status_code == HTTPStatus.OK


def test_add_new_crypto_page():
    with app.test_client() as test_client:
        with patch("app.application.create_session") as mock:
            mock.return_value = create_session()
            request = test_client.post("/add", data={"add": "Coin"})
            assert request.status_code == HTTPStatus.FOUND
            with create_session() as session:
                crypto = (
                    session.query(Cryptocurrency)
                    .filter(Cryptocurrency.name == "Coin")
                    .first()
                )
                assert crypto.price == "64"
                assert crypto.name == "Coin"


def test_login_page():
    with app.test_client() as test_client:
        with patch("app.application.create_session") as mock:
            mock.return_value = create_session()
            request = test_client.post("/login", data={"login": "Dmitriy"})
            assert request.status_code == HTTPStatus.FOUND
            with create_session() as session:
                user = session.query(User).filter(User.name == "Dmitriy").first()
                assert user.money == "1000"
                assert user.name == "Dmitriy"
