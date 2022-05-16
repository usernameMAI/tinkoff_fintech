from typing import AsyncGenerator

from sqlalchemy.orm import Session

from app.db.session import get_session


async def get_db() -> AsyncGenerator[Session, None]:
    db = get_session()()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
