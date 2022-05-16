import datetime
import random
import time
from decimal import Decimal

from app.databases import Cryptocurrency, create_session

updates = {'last_update': datetime.datetime.now()}


def update_costs() -> None:  # pragma: no cover
    """
    Функция обновляет каждые 10 секунд БД.
    Либо увеличивает, либо уменьшает
    на 1-10% каждую валюту.
    """
    while True:
        time.sleep(10)
        with create_session() as session:
            cryptos = session.query(Cryptocurrency).all()
            for crypto in cryptos:
                trend = random.randint(0, 1)
                delta = random.randint(1, 10)
                if trend:
                    coefficient = 1 + delta / 100
                    crypto.price = str(
                        Decimal(crypto.price) * Decimal(str(coefficient))
                    )
                else:
                    coefficient = 1 - delta / 100
                    crypto.price = str(
                        Decimal(crypto.price) * Decimal(str(coefficient))
                    )
            session.commit()
        updates['last_update'] = datetime.datetime.now()
