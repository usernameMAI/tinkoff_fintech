from typing import Union

from fastapi import HTTPException
from pydantic import BaseModel, validator


class NewUser(BaseModel):
    name: str
    password: str

    @validator("name")
    def check_name(cls, value: str) -> Union[str, HTTPException]:
        """
        Проверяет имя:
        она должно быть не пустым и
        его длина должна быть <= 15
        """
        if not value or value.isspace():
            raise HTTPException(status_code=400, detail="Name must not be empty")
        if len(value) > 15:
            raise HTTPException(
                status_code=400, detail="Name must be less than 15 characters long"
            )
        return value

    @validator("password")
    def check_password(cls, value: str) -> Union[str, HTTPException]:
        """
        Проверяет пароль:
        он должен быть не пустым,
        его длина должна быть <= 15
        """
        if not value or value.isspace():
            raise HTTPException(status_code=400, detail="Password must not be empty")
        if len(value) > 15:
            raise HTTPException(
                status_code=400,
                detail="Password must be" " less than 15 characters long",
            )
        return value


class NewFilm(BaseModel):
    title: str
    year: int
    month: int

    @validator("title")
    def check_title(cls, value: str) -> Union[str, HTTPException]:
        """
        Проверяет заголовок:
        он должен быть не пустым,
        его длина должна быть <= 15
        """
        if not value or value.isspace():
            raise HTTPException(status_code=400, detail="Film title must not be empty")
        if len(value) > 15:
            raise HTTPException(
                status_code=400,
                detail="Film title must be less than 15 characters long",
            )
        return value

    @validator("year")
    def check_year(cls, value: int) -> Union[int, HTTPException]:
        """
        Проверяет корректность года:
        он должен быть не отрицательным
        и не пустым
        """
        if value < 0:
            raise HTTPException(status_code=400, detail="Year cannot be less than zero")
        return value

    @validator("month")
    def check_month(cls, value: int) -> Union[int, HTTPException]:
        """
        Проверяет корректность месяца:
        он должен быть от 1 до 12,
        не пустым
        """
        if not value:
            raise HTTPException(status_code=400, detail="Month must not be empty")
        if value < 1 or value > 12:
            raise HTTPException(
                status_code=400, detail="Month must be between 1 and 12"
            )
        return value
