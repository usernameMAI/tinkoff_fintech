# pylint: disable=E1101
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from app.config import settings
from app.db.base import Base
from app.db.models import User, UserRole
from app.db.session import get_engine


def load_admins(session: Session) -> None:
    with open(settings.ADMIN_FILE, 'r', encoding='utf-8') as file:
        for line in file:
            login, password = line.split()
            user = session.query(User).filter_by(name=login).first()
            if not user:
                new_user = User(
                    name=login,
                    password=generate_password_hash(password),
                    role=UserRole.ADMIN,
                )  # type: ignore[call-arg]
                session.add(new_user)


def init_db(session: Session) -> None:
    Base.metadata.create_all(bind=get_engine())  # type: ignore[attr-defined]
    load_admins(session)
    session.commit()
