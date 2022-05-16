from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_user_from_db
from app.db.get_db import get_db
from app.db.models import User
from app.endpoints.auth import oauth2_scheme
from app.exceptions import UserNotExists
from app.schemas import UserModel

router_about = APIRouter()


@router_about.get('/user/me', response_model=UserModel)
async def get_info_about_me(
    login: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
    user: Optional[User] = get_user_from_db(db, login)
    if not user:
        raise UserNotExists
    return UserModel(login=user.name, id=user.id)
