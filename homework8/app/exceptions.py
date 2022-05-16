from http import HTTPStatus

from fastapi import HTTPException

from app.config import settings

LoginIsEmpty = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST, detail='Login must not be empty'
)

PasswordIsEmpty = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST, detail='Password must not be empty'
)

LoginTooLong = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST,
    detail=f'Login must be less than {settings.MAX_LOGIN_LENGTH} characters long',
)

PasswordTooLong = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST,
    detail=f'Password must be less than {settings.MAX_PASSWORD_LENGTH} characters long',
)

UserAlreadyExists = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST,
    detail='User already exists',
)

UserNotExists = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST, detail='User does not exist'
)

IncorrectData = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST,
    detail='Incorrect username or password',
)

PostAlreadyExist = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST, detail='Post already exist'
)

PostNotExist = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST, detail='Post does not exist'
)

NotEnoughRights = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST, detail='You are not an author or an admin'
)

CommentNotExist = HTTPException(
    status_code=HTTPStatus.BAD_REQUEST, detail='Comment does not exist'
)
