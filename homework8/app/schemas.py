from datetime import datetime
from typing import Optional, Union

from fastapi import HTTPException
from pydantic import BaseModel, validator

from app.config import settings
from app.exceptions import LoginIsEmpty, LoginTooLong, PasswordIsEmpty, PasswordTooLong


class NewUser(BaseModel):
    login: str
    password: str

    @validator('login')
    def check_name_correct(cls, value: str) -> Union[str, HTTPException]:
        if not value or value.isspace():
            raise LoginIsEmpty
        if len(value) > settings.MAX_LOGIN_LENGTH:
            raise LoginTooLong
        return value

    @validator('password')
    def check_password_correct(cls, value: str) -> Union[str, HTTPException]:
        if not value or value.isspace():
            raise PasswordIsEmpty
        if len(value) > settings.MAX_PASSWORD_LENGTH:
            raise PasswordTooLong
        return value


class OutUser(BaseModel):
    login: str


class UserModel(BaseModel):
    login: str
    id: int


class TokenResponseModel(BaseModel):
    access_token: str


class NewPostResponseModel(BaseModel):
    id: int


class OutPost(BaseModel):
    id: int
    header: str
    text: str
    rating: int
    date: datetime
    photo: Optional[bytes]


class PostDeleteModel(BaseModel):
    status: str = 'successfully'
    id: int


class NewComment(BaseModel):
    text: str


class OutNewComment(BaseModel):
    id: int
    author_id: int
    post_id: int


class CommentResponseModel(BaseModel):
    id: int
    author_id: int
    text: str


class CommentDeleteModel(BaseModel):
    status: str = 'successfully'
    id: int


class GiveAdminResponseModel(BaseModel):
    status: str = 'successfully'
    id: int


class RatingResponseModel(BaseModel):
    status: str = 'successfully'
    rating: str
    post_id: int
