from app.database import Film


def key_rating(value: Film) -> float:
    """
    Функция-ключ для сортировки
    по рейтингу фильма
    """
    if not value.average_rating:
        return 0.0
    return value.average_rating


def key_date(value: Film) -> float:
    """
    Функция-ключ для сортировки
    по дате выхода
    """
    return value.year_release * 12 + value.month_release
