from typing import Any, List


def paginate(full_list: List[Any], objects_per_page: int, page: int) -> List[Any]:
    """
    Пагинация списка 'full_list'
    """
    if page is None:
        page = 1
    page = max(page, 1)
    if objects_per_page < 1:
        objects_per_page = 10
    list_with_paginate = full_list[
        (page - 1) * objects_per_page : page * objects_per_page
    ]
    return list_with_paginate
