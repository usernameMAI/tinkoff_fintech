from typing import Any, List

from app.config import settings


def paginate(
    full_list: List[Any],
    objects_per_page: int = settings.DEFAULT_POSTS_PER_PAGE,
    page: int = settings.START_PAGE,
) -> List[Any]:
    page = max(page, 1)
    if objects_per_page < 1:
        objects_per_page = 10
    list_with_paginate = full_list[
        (page - 1) * objects_per_page : page * objects_per_page
    ]
    return list_with_paginate
