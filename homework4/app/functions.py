import datetime
from decimal import Decimal

from flask import Flask

from app.databases import OperationsHistory, PortfolioItem, Session, User


def create_app() -> Flask:
    """
    Функция создаёт и возвращает объект Flask.
    """
    return Flask(__name__)


def need_update_page(update: datetime.datetime, page_update: datetime.datetime) -> bool:
    """
    Функция проверяет, нужно ли
    обновлять страницу, на которой
    находится пользователь. Если
    прошло больше 10 секунд с последнего
    обновления значений криптовалют, то
    возвращается True.
    """
    if (update - page_update).seconds > 10:
        return True
    return False


def user_have_money(user: User, crypto_cost: str) -> bool:
    """
    Функция проверяет, может ли пользователь купить валюту:
    если у него денег больше, чем стоит валюта, то возвращается
    True.
    """
    return Decimal(user.money) > Decimal(crypto_cost)


def login_correct(user_login: str) -> bool:
    """
    Функция принимает на вход 'login' пользователя.
    Если он не пустой, его длина меньше 20, то
    возвращается True.
    """
    if not user_login or user_login.isspace() or len(user_login) > 20:
        return False
    return True


def buy_crypto(
    user: User, crypto_cost: str, crypto_name: str, login: str, session: Session
) -> None:
    """
    Функция совершает покупке пользователем 'user' криптовалюты
    'crypto_name' стоимостью 'crypto_cost'.
    """
    user.money = str(Decimal(user.money) - Decimal(crypto_cost))
    element = (
        session.query(PortfolioItem)
        .filter_by(name_user=login)
        .filter_by(name_crypto=crypto_name)
        .first()
    )
    if not element:
        new_crypto_for_user = PortfolioItem(
            name_user=login, name_crypto=crypto_name, count=1
        )
        session.add(new_crypto_for_user)
    else:
        element.count += 1
    element_in_history = OperationsHistory(
        name_user=login,
        name_crypto=crypto_name,
        cost=crypto_cost,
        operation=True,
    )
    session.add(element_in_history)
