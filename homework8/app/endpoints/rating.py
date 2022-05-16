from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.get_db import get_db
from app.db.models import Like, Post, User, UserRating
from app.endpoints.auth import my_logger, oauth2_scheme
from app.exceptions import PostNotExist
from app.schemas import RatingResponseModel

router_rating = APIRouter()


@router_rating.put('/post/{post_id}/rate', response_model=RatingResponseModel)
async def rate_post(
    post_id: int,
    grade: bool,
    db: Session = Depends(get_db),
    login: str = Depends(oauth2_scheme),
) -> RatingResponseModel:
    user = db.query(User).filter_by(name=login).first()
    post = db.query(Post).filter_by(id=post_id).first()
    rating = db.query(Like).filter_by(author=user, post=post).first()
    if not post:
        raise PostNotExist
    grade_in_db = UserRating.DISLIKE
    if grade:
        grade_in_db = UserRating.LIKE
    # если пользователь еще не оценивал, то просто добавляем оценку в БД
    if not rating:
        rating = Like(rating=grade_in_db, author=user, post=post)  # type: ignore[call-arg]
        db.add(rating)
        if grade:
            post.rating += 1
        else:
            post.rating -= 1
    # если пользователь уже ставил оценку к посту и она не совпадает с новой, то
    # нужно сменить оценку
    elif rating.rating != grade_in_db:
        if grade:
            post.rating += 2
        else:
            post.rating -= 2
        rating.rating = grade_in_db
    db.commit()
    my_logger.debug('User %s rated post %d.', login, post_id)
    return RatingResponseModel(rating=grade_in_db, post_id=post_id)
