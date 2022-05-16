import datetime
from decimal import Decimal
from typing import Union

import werkzeug.wrappers.response
from flask import redirect, render_template, request, url_for

from app.databases import (
    Cryptocurrency,
    OperationsHistory,
    PortfolioItem,
    User,
    create_session,
)
from app.functions import (
    buy_crypto,
    create_app,
    login_correct,
    need_update_page,
    user_have_money,
)
from app.paginate import paginate
from app.update_crypto_costs import updates

app = create_app()
login = ''


@app.route('/')
def start_page() -> str:
    """
    Стартовая страница. Возвращает html код,
    указанный в шаблоне base.html.
    """
    return render_template('base.html')


@app.route('/home')
def home_page() -> Union[str, werkzeug.wrappers.response.Response]:
    """
    Домашняя страница. Возвращает html код,
    указанный в шаблоне home.html.
    """
    if not login or login.isspace():
        return redirect(url_for('start_page'))
    with create_session() as session:
        money = session.query(User).filter_by(name=login).first().money
        return render_template('home.html', login=login, money=money)


@app.route('/login', methods=['POST'])
def login_page() -> Union[str, werkzeug.wrappers.response.Response]:
    """
    Функция вызывается, когда клиент нажал
    на кнопку login. Сохраняет пользователя
    в БД с начальным капиталом 1000.
    Перенаправляет на домашнюю страницу.
    """
    global login
    login = str(request.form.get('login'))
    if not login_correct(login):
        redirect(url_for('start_page'))
    with create_session() as session:
        user = session.query(User.name).filter(User.name == login).first()
        if not user:
            new_user = User(name=login, money='1000')
            session.add(new_user)
    return redirect(url_for('home_page'))


@app.route('/history/<int:page>')
@app.route('/history')
def history_page(page: int = 1) -> str:
    """
    Страница с историей операций клиента.
    Возвращает html код,
    указанный в шаблоне history.html.
    """
    with create_session() as session:
        history = session.query(OperationsHistory).filter_by(name_user=login).all()
        money = session.query(User).filter_by(name=login).first().money
        paginate_list, prev_page, next_page = paginate(history, page)
        next_url = url_for('history_page', page=page + 1)
        prev_url = url_for('history_page', page=page - 1)
        return render_template(
            'history.html',
            login=login,
            history=paginate_list,
            money=money,
            next=next_page,
            prev=prev_page,
            next_url=next_url,
            prev_url=prev_url,
        )


@app.route('/portfolio')
def portfolio_page() -> Union[str, werkzeug.wrappers.response.Response]:
    """
    Страница с валютами клиента, где клиент
    может посмотреть валюты или продать имеющуюся.
    Возвращает html код,
    указанный в шаблоне portfolio.html.
    """
    if not login_correct(login):
        return redirect(url_for('start_page'))
    updates['last_sell_update'] = datetime.datetime.now()
    with create_session() as session:
        user_cryptos = session.query(PortfolioItem).filter_by(name_user=login).all()
        user_money = session.query(User).filter_by(name=login).first().money
        prices = {}
        for element in user_cryptos:
            crypto = (
                session.query(Cryptocurrency)
                .filter_by(name=element.name_crypto)
                .first()
            )
            prices[crypto.name] = crypto.price
        return render_template(
            'portfolio.html',
            login=login,
            money=user_money,
            cryptos=user_cryptos,
            prices=prices,
        )


@app.route('/portfolio/<string:crypto_name>', methods=['POST'])
def portfolio_sell_page(
    crypto_name: str,
) -> Union[str, werkzeug.wrappers.response.Response]:
    """
    Функция вызывается, когда клиент нажал
    на кнопку sell. Удаляет у пользователя
    одну единицу валюты 'crypto_name' и
    увеличивает его баланс на её стоимость.
    Перенаправляет на страницу с валютами клиента.
    """
    if not need_update_page(updates['last_sell_update'], updates['last_update']):
        with create_session() as session:
            user = session.query(User).filter_by(name=login).first()
            crypto_cost = (
                session.query(Cryptocurrency).filter_by(name=crypto_name).first().price
            )
            element = (
                session.query(PortfolioItem)
                .filter_by(name_user=login)
                .filter_by(name_crypto=crypto_name)
                .first()
            )
            element_in_history = OperationsHistory(
                name_user=login,
                name_crypto=crypto_name,
                cost=crypto_cost,
                operation=False,
            )
            session.add(element_in_history)
            if element.count > 0:
                element.count -= 1
                user.money = str(Decimal(user.money) + Decimal(crypto_cost))
            if not element.count:
                session.delete(element)
    return redirect(url_for('portfolio_page'))


@app.route('/buy')
def buy_page() -> Union[str, werkzeug.wrappers.response.Response]:
    """
    Страница с магазином, где клиент
    может купить или добавить новую валюту.
    Возвращает html код,
    указанный в шаблоне buy.html.
    """
    if not login_correct(login):
        return redirect(url_for('start_page'))
    updates['last_buy_update'] = datetime.datetime.now()
    with create_session() as session:
        values = session.query(Cryptocurrency).all()
        money = session.query(User).filter_by(name=login).first().money
        return render_template('buy.html', login=login, money=money, values=values)


@app.route('/buy/<string:crypto_name>', methods=['POST'])  # pragma: no cover
def buy_crypto_page(
    crypto_name: str,
) -> Union[str, werkzeug.wrappers.response.Response]:
    """
    Функция вызывается, когда клиент нажал
    на кнопку buy. Если у пользователя
    достаточно денег для покупки валюты, то
    её количество у него увеличивается на 1.
    Перенаправляет на страницу покупок.
    """
    if not login_correct(login):
        return redirect(url_for('start_page'))
    if not need_update_page(updates['last_buy_update'], updates['last_update']):
        with create_session() as session:
            user = session.query(User).filter_by(name=login).first()
            crypto_cost = (
                session.query(Cryptocurrency).filter_by(name=crypto_name).first().price
            )
            if user_have_money(user, crypto_cost):
                buy_crypto(user, crypto_cost, crypto_name, login, session)
    return redirect(url_for('buy_page'))


@app.route('/add', methods=['POST'])
def add_new_crypto_page() -> Union[str, werkzeug.wrappers.response.Response]:
    """
    Функция вызывается, когда клиент нажал
    на кнопку add. Добавляет валюту в БД,
    если её там нет.
    Перенаправляет на страницу покупок.
    """
    name = request.form.get('add')
    with create_session() as session:
        find_crypto = (
            session.query(Cryptocurrency.name)
            .filter(Cryptocurrency.name == name)
            .first()
        )
        if not name or name.isspace() or find_crypto:
            return redirect(url_for('buy_page'))
        crypto = Cryptocurrency(name=name, price='64')
        session.add(crypto)
    return redirect(url_for('buy_page'))
