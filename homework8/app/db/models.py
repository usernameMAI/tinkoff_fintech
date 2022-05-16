import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    CLIENT = 'client'
    ADMIN = 'admin'


class UserRating(str, enum.Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'


class User(Base):
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default=UserRole.CLIENT, nullable=False)


class Post(Base):
    author_id = Column(Integer, ForeignKey('user.id'))
    header = Column(String, nullable=False)

    text = Column(String, nullable=False)
    photo = Column(LargeBinary, nullable=True)
    date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    rating = Column(Integer, default=0, nullable=False)

    author = relationship('User')

    __table_args__ = (
        UniqueConstraint('author_id', 'header', name='author_id_header_uc'),
    )


class Comment(Base):
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    text = Column(String, nullable=False)

    author = relationship('User')
    post = relationship('Post')


class Like(Base):
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    rating = Column(String, nullable=False)

    author = relationship('User')
    post = relationship('Post')

    __table_args__ = (
        UniqueConstraint(
            'author_id', 'post_id', 'rating', name='author_id_post_id_rating_uc'
        ),
    )
