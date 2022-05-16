# pylint: disable=missing-module-docstring
import datetime
import shelve


def get_datetime(file: dict, city: str) -> datetime:
    """
    Функция возвращает объект типа datetime,
    который сохранён в файле 'file'.
    """
    return file[city][0]


def get_temperature(file: dict, city: str) -> str:
    """
    Функция возвращает строку формата
    'температура' + 'знак градуса цельсия',
    которая сохранена в файле 'file'.
    """
    return file[city][1]


def need_cache(file: dict, city: str, cache_seconds=300) -> bool:
    """
    Функция проверяет, нужно ли кэшировать данные.
    Если прошло больше 5 минут с кэширования температуры города city,
    либо его ещё не было, то функция вернёт True, иначе False.
    """
    return \
        file.get(city) is None\
        or (datetime.datetime.now() -
            get_datetime(file, city)).total_seconds() > cache_seconds


def cache(func):
    """
    Декоратор для кэширования.
    Для правильной работы первой аргумент
    функции должен быть городом.
    """
    def wrapper(*args, **kwargs):
        filename = "cache"
        # чтобы были одинаковы такие случаи: 'moscow' и 'Moscow'
        city = args[0].lower()
        # файл открывается "как словарь"
        with shelve.open(filename) as file:
            # если кэширования не было, либо после него прошло больше 5 минут
            if need_cache(file, city):
                temperature = func(*args, **kwargs)
                if temperature != "Error":
                    file[city] = (datetime.datetime.now(), temperature)
            else:
                temperature = get_temperature(file, city)
            return temperature
    return wrapper
