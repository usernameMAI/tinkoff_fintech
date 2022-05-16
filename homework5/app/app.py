from typing import Dict, List, Union

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from werkzeug.security import generate_password_hash

from app.database import Base, Film, RateHistory, ReviewHistory, User, engine
from app.functions import (
    authenticate_user,
    change_film_rating,
    convert_to_common_list,
    create_session,
    rating_correct,
)
from app.keys import key_date, key_rating
from app.models import NewFilm, NewUser
from app.paginate import paginate

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Base.metadata.create_all(engine)


@app.post("/register")
def register(new_user: NewUser) -> Union[Dict[str, str], HTTPException]:
    """
    Регистрация пользователя
    """
    with create_session() as session:
        user = session.query(User).filter_by(name=new_user.name).first()
        if user:
            raise HTTPException(status_code=400, detail="User already registered")
        secure_password = generate_password_hash(new_user.password)
        user = User(name=new_user.name, password=secure_password)
        session.add(user)
        return {"Status": "ok"}


@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Union[Dict[str, str], HTTPException]:
    """
    Авторизация пользователя
    """
    username = form_data.username
    password = form_data.password
    if authenticate_user(username, password):
        return {"access_token": username}
    raise HTTPException(status_code=400, detail="Incorrect username or password")


@app.post("/add")
def add_film(
    new_film: NewFilm, token: str = Depends(oauth2_scheme)
) -> Union[Dict[str, str], HTTPException]:
    """
    Добавить фильм в БД без оценки
    """
    with create_session() as session:
        film = (
            session.query(Film)
            .filter_by(
                title=new_film.title,
                year_release=new_film.year,
                month_release=new_film.month,
            )
            .first()
        )
        if film:
            raise HTTPException(status_code=400, detail="Film already exists")
        film = Film(
            title=new_film.title,
            year_release=new_film.year,
            month_release=new_film.month,
        )
        session.add(film)
        return {"Status": "ok"}


@app.post("/review/{title}")
def save_film_review(
    title: str,
    year: int,
    month: int,
    new_review: str,
    token: str = Depends(oauth2_scheme),
) -> Union[Dict[str, str], HTTPException]:
    """
    Добавить отзыв к фильму
    Если отзыв уже есть, то он обновляется на новый
    """
    with create_session() as session:
        film = (
            session.query(Film)
            .filter_by(title=title, year_release=year, month_release=month)
            .first()
        )
        if not film:
            raise HTTPException(status_code=400, detail="Film not exists")
        film_review_in_history = (
            session.query(ReviewHistory)
            .filter_by(film_title=title, user_name=token)
            .first()
        )
        if film_review_in_history:
            film.count_review -= 1
            session.delete(film_review_in_history)
        review_in_history = ReviewHistory(
            user_name=token, film_title=title, review=new_review
        )
        session.add(review_in_history)
        film.count_review += 1
        session.commit()
        return {"Status": "ok"}


@app.put("/rate/{title}/{rating}")
def rate_film(
    title: str,
    year: int,
    month: int,
    rating: int,
    token: str = Depends(oauth2_scheme),
) -> Union[Dict[str, str], HTTPException]:
    """
    Добавить оценку фильму от 1 до 10
    Если оценка уже есть, то оценка обновляется
    """
    with create_session() as session:
        film = (
            session.query(Film)
            .filter_by(title=title, year_release=year, month_release=month)
            .first()
        )
        if not film:
            raise HTTPException(status_code=400, detail="Film not exists")
        if not rating_correct(rating):
            raise HTTPException(status_code=400, detail="Rating must be from 1 to 10")
        change_film_rating(film, rating, token, session)
        history = RateHistory(user_name=token, film_title=title, rating=rating)
        session.add(history)
        session.commit()
        return {"Status": "ok"}


@app.get("/films")
def films(
    films_per_page: int = 10, page: int = 1, token: str = Depends(oauth2_scheme)
) -> Dict[str, Union[str, List[str]]]:
    """
    Список фильмов по порядку добавления в БД
    """
    with create_session() as session:
        request = session.query(Film).all()
        if not request:
            return {"Status": "ok"}
        list_films = convert_to_common_list(request)
        return {"Status": "ok", "data": paginate(list_films, films_per_page, page)}


@app.get("/films/rating/top")
def films_top_rating(
    films_per_page: int = 10, page: int = 1, token: str = Depends(oauth2_scheme)
) -> Dict[str, Union[str, List[str]]]:
    """
    Список фильмов по рейтингу
    """
    with create_session() as session:
        request = session.query(Film).all()
        if not request:
            return {"Status": "ok"}
        list_films = convert_to_common_list(
            sorted(request, key=key_rating, reverse=True)
        )
        return {"Status": "ok", "data": paginate(list_films, films_per_page, page)}


@app.get("/films/rating/date")
def films_top_date(
    films_per_page: int = 10, page: int = 1, token: str = Depends(oauth2_scheme)
) -> Dict[str, Union[str, List[str]]]:
    """
    Список фильмов по дате выхода
    """
    with create_session() as session:
        request = session.query(Film).all()
        if not request:
            return {"Status": "ok"}
        list_films = convert_to_common_list(
            sorted(request, key=key_date, reverse=False)
        )
        return {"Status": "ok", "data": paginate(list_films, films_per_page, page)}


@app.get("/films/{substring}")
def find_films_substring(
    substring: str,
    films_per_page: int = 10,
    page: int = 1,
    token: str = Depends(oauth2_scheme),
) -> Dict[str, Union[str, List[str]]]:
    """
    Список фильмов с подстрокой 'substring'
    """
    with create_session() as session:
        request = session.query(Film).filter(Film.title.contains(substring)).all()
        if not request:
            return {"Status": "ok"}
        list_films = convert_to_common_list(request)
        return {"Status": "ok", "data": paginate(list_films, films_per_page, page)}


@app.get("/about/{title}")
def about_film(
    title: str, year: int, month: int, token: str = Depends(oauth2_scheme)
) -> Union[HTTPException, Dict[str, Union[str, float]]]:
    """
    Информация о фильме:
    рейтинг, сколько оценок, сколько отзывов
    """
    with create_session() as session:
        film = (
            session.query(Film)
            .filter_by(title=title, year_release=year, month_release=month)
            .first()
        )
        if not film:
            raise HTTPException(status_code=400, detail="Film not exists")
        return {
            "Status": "ok",
            "title": title,
            "rating": film.average_rating,
            "count_rating": film.count_rating,
            "count_review": film.count_review,
        }


@app.get("/films/review/{title}")
def film_reviews(
    title: str,
    year: int,
    month: int,
    films_per_page: int = 10,
    page: int = 1,
    token: str = Depends(oauth2_scheme),
) -> Union[Dict[str, Union[str, List[str]]], HTTPException]:
    """
    Список всех отзывов о фильме
    """
    with create_session() as session:
        film = (
            session.query(Film)
            .filter_by(title=title, year_release=year, month_release=month)
            .first()
        )
        if not film:
            raise HTTPException(status_code=400, detail="Film not exists")
        reviews = session.query(ReviewHistory).filter_by(film_title=title).all()
        reviews_list = []
        for review in reviews:
            reviews_list.append(
                {
                    "user": review.user_name,
                    "title": review.film_title,
                    "review": review.review,
                }
            )
        return {"Status": "ok", "reviews": paginate(reviews_list, films_per_page, page)}
