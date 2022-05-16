from base64 import b64encode
from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import Comment, Post, User, UserRole


def user_post_already_exist(db: Session, header: str, user: User) -> bool:
    post_in_db = db.query(Post).filter_by(header=header, author=user).first()
    return post_in_db is not None


def encode_photo(photo: Optional[bytes]) -> Optional[bytes]:
    if photo is None:
        return None
    return b64encode(photo)


def user_can_delete_post(db: Session, user: str, post: Post) -> bool:
    user_in_db = db.query(User).filter_by(name=user).first()
    return user_in_db.role == UserRole.ADMIN or post.author == user_in_db


def user_can_delete_comment(db: Session, user: str, comment: Comment) -> bool:
    user_in_db = db.query(User).filter_by(name=user).first()
    return user_in_db.role == UserRole.ADMIN or comment.author == user_in_db
