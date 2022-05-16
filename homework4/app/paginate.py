import math
from typing import List, Tuple, Union

from app.databases import OperationsHistory


def paginate(
    history: List[OperationsHistory], page: Union[None, int], post_per_page: int = 10
) -> Tuple[List[OperationsHistory], Union[None, int], Union[None, int]]:
    """
    Функция преобразует список всей истории в список из
    'POSTS_PER_PAGE' элементов. Возвращает кортеж с
    новым списком, номерами предыдущей и следующей страницы.
    """
    if page is None:
        page = 1
    else:
        page = int(page)
    length = len(history)
    history = history[(page - 1) * post_per_page : page * post_per_page]
    if page > 1:
        prev_page = page - 1
    else:
        prev_page = None
    if page < math.ceil(length / post_per_page):
        next_page = page + 1
    else:
        next_page = None
    return history, prev_page, next_page
