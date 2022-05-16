from contextlib import contextmanager
from typing import Any, Dict, List, Union

from werkzeug.security import check_password_hash

from app.database import Film, RateHistory, Session, User


@contextmanager
def create_session(**kwargs: Any) -> Session:  # pragma: no cover
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


def authenticate_user(username: str, password: str) -> bool:
    """
    Функция проверяет, есть ли пользователь в БД.
    Если есть, то проверяет, совпадает ли пароль с паролем в БД.
    """
    with create_session() as session:
        user_in_db = session.query(User).filter_by(name=username).first()
        if user_in_db:
            password_check = check_password_hash(user_in_db.password, password)
            return password_check
        return False


def rating_correct(rating: int) -> bool:
    """
    Функция проверяет, корректный ли рейтинг
    (должен быть от 1 до 10)
    """
    if rating < 1 or rating > 10:
        return False
    return True


def change_film_rating(
    film: Film, new_rating: int, user_name: str, session: Session
) -> None:
    """
    Функция меняет сохраненное в БД значение оценки фильма
    пользователя на новое, либо добавляет новое
    """
    film_rate_in_history = (
        session.query(RateHistory)
        .filter_by(film_title=film.title, user_name=user_name)
        .first()
    )

    if film_rate_in_history:
        film.count_rating -= 1
        film.rating -= film_rate_in_history.rating
        session.delete(film_rate_in_history)
    film.count_rating += 1
    film.rating += new_rating
    film.average_rating = round((film.rating / film.count_rating), 3)


def convert_to_common_list(
    request: List[Film],
) -> List[Dict[str, Union[int, float, None]]]:
    """
    Функция создаёт новый список, который
    не связан с БД
    """
    films = []
    for element in request:
        film = {
            "title": element.title,
            "rating": element.average_rating,
            "count_rating": element.count_rating,
            "count_review": element.count_review,
            "year_release": element.year_release,
            "month_release": element.month_release,
        }
        films.append(film)
    return films
