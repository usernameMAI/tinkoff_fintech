import pytest
from fastapi import HTTPException

from app.schemas import NewUser


def test_new_user():
    new_user = NewUser(login='test', password='test')
    assert new_user.login == 'test'
    assert new_user.password == 'test'


def test_new_user_with_empty_login():
    with pytest.raises(HTTPException):
        NewUser(login='', password='test')


def test_new_user_with_empty_password():
    with pytest.raises(HTTPException):
        NewUser(login='test', password='')


def test_new_user_with_long_name():
    with pytest.raises(HTTPException):
        NewUser(login='12345123451234512345', password='test')


def test_new_user_with_long_password():
    with pytest.raises(HTTPException):
        NewUser(login='test', password='12345123451234512345')
