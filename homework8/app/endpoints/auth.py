# type: ignore[call-arg]
import logging

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from app.auth import add_user_in_db, check_correct_user_to_auth, get_user_from_db
from app.config import settings
from app.db.get_db import get_db
from app.db.models import User, UserRole
from app.exceptions import (
    IncorrectData,
    NotEnoughRights,
    UserAlreadyExists,
    UserNotExists,
)
from app.schemas import GiveAdminResponseModel, NewUser, OutUser, TokenResponseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
logging.basicConfig(level=logging.DEBUG, filename=settings.FILE_LOGS_NAME, filemode='w')
my_logger = logging.getLogger(__name__)
router_auth = APIRouter()


@router_auth.post('/register', response_model=OutUser)
async def register(user: NewUser, db: Session = Depends(get_db)) -> OutUser:
    user_in_db = get_user_from_db(db, user.login)
    if user_in_db:
        raise UserAlreadyExists
    new_user = User(name=user.login, password=generate_password_hash(user.password))
    add_user_in_db(db, new_user)
    my_logger.debug('User %s with id %d has registered.', user.login, new_user.id)
    return OutUser(login=user.login)


@router_auth.post('/token', response_model=TokenResponseModel)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> TokenResponseModel:  # pragma: no cover
    user_exist = check_correct_user_to_auth(db, form_data.username, form_data.password)
    if user_exist:
        my_logger.debug('User %s has entered.', form_data.username)
        return TokenResponseModel(access_token=form_data.username)
    raise IncorrectData


@router_auth.put('/admin/{user_id}', response_model=GiveAdminResponseModel)
async def give_admin(
    user_id: int, db: Session = Depends(get_db), user: str = Depends(oauth2_scheme)
) -> GiveAdminResponseModel:
    i_in_db = db.query(User).filter_by(name=user).first()
    user_in_db = db.query(User).filter_by(id=user_id).first()
    if not user_in_db:
        raise UserNotExists
    if i_in_db.role != UserRole.ADMIN:
        raise NotEnoughRights
    user_in_db.role = UserRole.ADMIN
    db.commit()
    return GiveAdminResponseModel(id=user_id)
