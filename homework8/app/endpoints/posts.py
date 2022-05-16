# type: ignore[valid-type]

import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form
from pydantic import conint
from sqlalchemy.orm import Session

from app.config import settings
from app.db.get_db import get_db
from app.db.models import Comment, Like, Post, User
from app.db_check import encode_photo, user_can_delete_post, user_post_already_exist
from app.endpoints.auth import my_logger, oauth2_scheme
from app.exceptions import NotEnoughRights, PostAlreadyExist, PostNotExist
from app.paginate import paginate
from app.schemas import NewPostResponseModel, OutPost, PostDeleteModel

router_posts = APIRouter()


@router_posts.post('/post', response_model=NewPostResponseModel)
async def add_post(
    photo: Optional[bytes] = File(None),
    header: str = Form(...),
    text: str = Form(...),
    db: Session = Depends(get_db),
    login: str = Depends(oauth2_scheme),
) -> NewPostResponseModel:
    user_in_db = db.query(User).filter_by(name=login).first()
    if user_post_already_exist(db, header, user_in_db):
        raise PostAlreadyExist
    post = Post(header=header, text=text, photo=photo, author=user_in_db)  # type: ignore[call-arg]
    db.add(post)
    db.commit()
    my_logger.debug('User %s added a post with id %d.', user_in_db.name, post.id)
    return NewPostResponseModel(id=post.id)


@router_posts.delete('/post/{post_id}/delete', response_model=PostDeleteModel)
async def delete_post_by_id(
    post_id: int, db: Session = Depends(get_db), login: str = Depends(oauth2_scheme)
) -> PostDeleteModel:
    post = db.query(Post).filter_by(id=post_id).first()
    user = db.query(User).filter_by(name=login).first()
    if not post:
        raise PostNotExist
    if not user_can_delete_post(db, login, post):
        raise NotEnoughRights
    comments = db.query(Comment).filter_by(post_id=post_id).all()
    likes = db.query(Like).filter_by(post=post, author=user).all()
    for comment in comments:
        db.delete(comment)
    for like in likes:
        db.delete(like)
    db.delete(post)
    my_logger.debug('User %s deleted post with id %d.', login, post_id)
    return PostDeleteModel(id=post.id)


@router_posts.get('/post/{post_id}', response_model=OutPost)
async def get_post_by_id(post_id: int, db: Session = Depends(get_db)) -> OutPost:
    post = db.query(Post).filter_by(id=post_id).first()
    if not post:
        raise PostNotExist
    out_photo = encode_photo(post.photo)
    return OutPost(
        id=post.id,
        header=post.header,
        text=post.text,
        rating=post.rating,
        date=post.date,
        photo=out_photo,
    )


@router_posts.get('/user/{user_id}/post', response_model=List[OutPost])
async def get_user_posts(
    user_id: int,
    posts_per_page: conint(gt=0) = settings.DEFAULT_POSTS_PER_PAGE,
    page: conint(gt=0) = settings.START_PAGE,
    db: Session = Depends(get_db),
) -> List[OutPost]:
    posts = db.query(Post).filter_by(author_id=user_id).all()
    return [
        OutPost(
            id=post.id,
            header=post.header,
            text=post.text,
            rating=post.rating,
            date=post.date,
            photo=post.photo,
        )
        for post in paginate(posts, posts_per_page, page)
    ]


@router_posts.get('/posts/last_day', response_model=List[OutPost])
async def get_last_day_posts(
    posts_per_page: conint(gt=0) = settings.DEFAULT_POSTS_PER_PAGE,
    page: conint(gt=0) = settings.START_PAGE,
    db: Session = Depends(get_db),
) -> List[OutPost]:
    date_delta = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    posts = db.query(Post).filter(Post.date >= date_delta).all()
    return [
        OutPost(
            id=post.id,
            header=post.header,
            text=post.text,
            rating=post.rating,
            date=post.date,
            photo=post.photo,
        )
        for post in paginate(posts, posts_per_page, page)
    ]
