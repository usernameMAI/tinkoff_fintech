from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.get_db import get_db
from app.db.models import Comment, Post, User
from app.db_check import user_can_delete_comment
from app.endpoints.auth import my_logger, oauth2_scheme
from app.exceptions import CommentNotExist, NotEnoughRights, PostNotExist
from app.schemas import (
    CommentDeleteModel,
    CommentResponseModel,
    NewComment,
    OutNewComment,
)

router_comments = APIRouter()


@router_comments.post('/post/{post_id}/comment', response_model=OutNewComment)
async def add_comment(
    post_id: int,
    new_comment: NewComment,
    db: Session = Depends(get_db),
    login: str = Depends(oauth2_scheme),
) -> OutNewComment:
    user = db.query(User).filter_by(name=login).first()
    post = db.query(Post).filter_by(id=post_id).first()
    if not post:
        raise PostNotExist
    comment = Comment(text=new_comment.text, post=post, author=user)  # type: ignore[call-arg]
    db.add(comment)
    db.commit()
    my_logger.debug(
        'User %s added a comment %s with id %d to the post %d.',
        user.name,
        new_comment.text,
        comment.id,
        post_id,
    )
    return OutNewComment(id=comment.id, author_id=user.id, post_id=post_id)


@router_comments.delete(
    '/post/{post_id}/comment/{comment_id}', response_model=CommentDeleteModel
)
async def delete_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(oauth2_scheme),
) -> CommentDeleteModel:
    comment = db.query(Comment).filter_by(id=comment_id, post_id=post_id).first()
    if not comment:
        raise CommentNotExist
    if not user_can_delete_comment(db, user, comment):
        raise NotEnoughRights
    db.delete(comment)
    my_logger.debug(
        'User %s deleted a comment %d from the post %d.', user, comment_id, post_id
    )
    return CommentDeleteModel(id=comment_id)


@router_comments.get(
    '/post/{post_id}/comments', response_model=List[CommentResponseModel]
)
async def get_comments(
    post_id: int,
    db: Session = Depends(get_db),
) -> List[CommentResponseModel]:
    comments = db.query(Comment).filter_by(post_id=post_id).all()
    return [
        CommentResponseModel(
            id=comment.id, author_id=comment.author_id, text=comment.text
        )
        for comment in comments
    ]
