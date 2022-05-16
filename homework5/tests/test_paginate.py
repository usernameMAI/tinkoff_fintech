import pytest

from app.paginate import paginate


@pytest.fixture()
def my_list():
    return [1, 2, 3, 4, 5]


def test_paginate_with_one_page(my_list):
    paginate_list = paginate(my_list, 10, 1)
    assert len(paginate_list) == 5


def test_paginate_with_five_page(my_list):
    paginate_list = paginate(my_list, 1, 5)
    assert len(paginate_list) == 1


def test_paginate_with_negative_objects_per_page(my_list):
    paginate_list = paginate(my_list, -5, 1)
    assert len(paginate_list) == 5
