from contextlib import contextmanager
from functools import lru_cache
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False)


@lru_cache()
def get_engine() -> Engine:
    return create_engine(settings.DATABASE_URL)


@lru_cache()
def get_session() -> sessionmaker:
    SessionLocal.configure(bind=get_engine())
    return SessionLocal


@contextmanager
def create_session() -> Iterator[Session]:  # pragma: no cover
    session = get_session()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
