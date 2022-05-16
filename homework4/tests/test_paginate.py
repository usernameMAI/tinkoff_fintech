import pytest

from app.databases import OperationsHistory
from app.paginate import paginate


@pytest.fixture()
def history():
    operations_history1 = OperationsHistory(
        id=1, name_user="USER", name_crypto="CRYPTO", cost="1", operation=True
    )
    operations_history2 = OperationsHistory(
        id=2, name_user="USER", name_crypto="CRYPTO", cost="1", operation=True
    )
    operations_history3 = OperationsHistory(
        id=3, name_user="USER", name_crypto="CRYPTO", cost="1", operation=True
    )
    history = [operations_history1, operations_history2, operations_history3]
    return history


def test_paginate_without_prev_page(history):
    page = 1
    post_per_page = 1
    history_page, prev_page, next_page = paginate(history, page, post_per_page)
    assert len(history_page) == 1
    assert prev_page is None
    assert next_page == 2


def test_paginate_without_next_page(history):
    page = 3
    post_per_page = 1
    history_page, prev_page, next_page = paginate(history, page, post_per_page)
    assert len(history_page) == 1
    assert prev_page == 2
    assert next_page is None


def test_paginate_with_pages(history):
    page = 2
    post_per_page = 1
    history_page, prev_page, next_page = paginate(history, page, post_per_page)
    assert len(history_page) == 1
    assert prev_page == 1
    assert next_page == 3


def test_paginate_with_one_page(history):
    page = 1
    history_page, prev_page, next_page = paginate(history, page)
    assert len(history_page) == 3
    assert prev_page is None
    assert next_page is None


def test_paginate_with_none_page(history):
    history_page, prev_page, next_page = paginate(history, None)
    assert len(history_page) == 3
    assert prev_page is None
    assert next_page is None
