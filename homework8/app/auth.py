from typing import Optional

from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from app.db.models import User


def get_user_from_db(db: Session, user: str) -> Optional[User]:
    user_in_db = db.query(User).filter_by(name=user).first()
    return user_in_db


def add_user_in_db(db: Session, user: User) -> None:
    db.add(user)
    db.commit()


def check_correct_user_to_auth(db: Session, login: str, password: str) -> bool:
    user_in_db = get_user_from_db(db, login)
    return user_in_db is not None and check_password_hash(user_in_db.password, password)
