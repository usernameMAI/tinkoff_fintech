from contextlib import contextmanager
from typing import Any, Generator

from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()  # type: Any
engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)


@contextmanager
def create_session(
    **kwargs: Any,
) -> Generator[scoped_session, None, None]:  # pragma: no cover
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


class Cryptocurrency(Base):
    __tablename__ = 'cryptocurrency'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(String, nullable=False)


class PortfolioItem(Base):
    __tablename__ = 'storage'
    id = Column(Integer, nullable=False, primary_key=True)
    name_user = Column(String, nullable=False)
    name_crypto = Column(String, nullable=False)
    count = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    money = Column(String, nullable=False)


class OperationsHistory(Base):
    __tablename__ = 'history'
    id = Column(Integer, nullable=False, primary_key=True)
    name_user = Column(String, nullable=False)
    name_crypto = Column(String, nullable=False)
    cost = Column(String, nullable=False)
    # True - покупка, False - продажа
    operation = Column(Boolean, nullable=False)


def create_db() -> None:  # pragma: no cover
    Base.metadata.create_all(engine)
    # создание БД и добавление в неё криптовалют
    with create_session() as session:
        for i in range(1, 6):
            crypto = Cryptocurrency(name=f'Crypto{i}', price=str(2**i))
            q = session.query(Cryptocurrency.name).filter(
                Cryptocurrency.name == f'Crypto{i}'
            )
            if not session.query(q.exists()).scalar():
                session.add(crypto)
