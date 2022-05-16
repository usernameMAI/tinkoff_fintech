import datetime
from contextlib import contextmanager

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.databases import Base, OperationsHistory, PortfolioItem, User
from app.functions import buy_crypto, login_correct, need_update_page, user_have_money

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


def test_need_update_page_false():
    update = datetime.datetime(1000, 10, 10)
    page_update = datetime.datetime(1000, 10, 10)
    assert need_update_page(update, page_update) is False


def test_need_update_page_true():
    update = datetime.datetime(1000, 10, 10, 10, 0)
    page_update = datetime.datetime(1000, 10, 10, 11)
    assert need_update_page(update, page_update) is True


def test_user_have_money_true():
    user = User(id=1, name="user", money=1000)
    assert user_have_money(user, "1") is True


def test_user_have_money_false():
    user = User(id=1, name="user", money=1000)
    assert user_have_money(user, "10000") is False


def test_login_correct_true():
    login = "Dmitriy"
    assert login_correct(login) is True


def test_login_correct_false():
    login = ""
    assert login_correct(login) is False


def test_login_correct_login_too_long():
    login = "123456789012345678901234567890"
    assert login_correct(login) is False


def test_buy_crypto():
    user = User(id=1, name="Dmitriy", money="1000")
    crypto_cost = "10"
    crypto_name = "Crypto1"
    login = "Dmitriy"
    with create_session() as session:
        buy_crypto(user, crypto_cost, crypto_name, login, session)
        assert user.money == "990"
    with create_session() as session:
        history = session.query(OperationsHistory).filter_by(name_user=login).first()
        user_crypto = session.query(PortfolioItem).filter_by(name_user=login).first()
        assert history.name_user == "Dmitriy"
        assert history.name_crypto == "Crypto1"
        assert history.cost == "10"
        assert history.operation == 1
        assert user_crypto.name_user == "Dmitriy"
        assert user_crypto.name_crypto == "Crypto1"
        assert user_crypto.count == 1
        buy_crypto(user, crypto_cost, crypto_name, login, session)
    with create_session() as session:
        user_crypto = session.query(PortfolioItem).filter_by(name_user=login).first()
        assert user_crypto.count == 2
