from typing import Any

from sqlalchemy import Column, Float, Integer, UniqueConstraint, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()  # type: Any
engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)


class RateHistory(Base):
    __tablename__ = "films_rating_history"
    id = Column(Integer, nullable=False, primary_key=True)
    user_name = Column(String, nullable=False)
    film_title = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)


class ReviewHistory(Base):
    __tablename__ = "films_review_history"
    id = Column(Integer, nullable=False, primary_key=True)
    user_name = Column(String, nullable=False)
    film_title = Column(String, nullable=False)
    review = Column(String, nullable=False)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Film(Base):
    __tablename__ = "film"
    __table_args__ = (
        UniqueConstraint(
            "title", "year_release", "month_release", name="film_title_date_release_key"
        ),
    )
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    year_release = Column(Integer, nullable=False)
    month_release = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False, default=0)
    count_rating = Column(Integer, nullable=False, default=0)
    count_review = Column(Integer, nullable=False, default=0)
    average_rating = Column(Float, nullable=True)
