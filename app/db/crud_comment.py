from sqlalchemy.orm import Session
from sqlalchemy import update, insert, select, delete

from app.db import schemas
from app.db.models import User, Group, Post, Comment
from app.db.utils import is_exist

def create_comment(
    db: Session,
    post_id: int,
    comment: schemas.CommentDTO
) -> Comment | None:
    author = is_exist(db, comment.author_id, User)
    post = is_exist(db, post_id, Post)
    if not author or not post:
        return None
    comment_dict = comment.model_dump()
    comment_dict['post_id'] = post_id
    db_comment = db.scalar(
        insert(Comment).returning(Comment),
        comment_dict
    )
    return db_comment

def get_post_comment_by_id(
    db: Session,
    post_id: int,
    comment_id: int
) -> Comment | None:
    post = is_exist(db, post_id, Post)
    if not post:
        return None
    return db.get(Comment, comment_id)

def get_all_post_comments(
    db: Session, 
    post_id: int
) -> list[Comment] | None:
    post = is_exist(db, post_id, Post)
    if not post:
        return None
    commets = db.scalars(
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at)
    ).all()
    return commets

def delete_comment(db: Session, post_id, comment_id) -> Comment | None:
    post = is_exist(db, post_id, Post)
    if not post:
        return None
    comment = db.scalar(
        delete(Comment).where(Comment.id == comment_id).returning(Comment)
    )
    return comment

def update_comment(
    db: Session,
    post_id: int,
    comment_id: int,
    new_comment_data: schemas.CommentUpdate
) -> Comment | None:
    post = is_exist(db, post_id, Post)
    comment = is_exist(db, comment_id, Comment) 
    if not post or not comment:
        return None
    new_data_dict = new_comment_data.model_dump(exclude_unset=True)
    stmt = (
        update(Comment)
        .where(Comment.id==comment_id)
        .values(**new_data_dict)
        .returning(Comment)
    )
    return db.scalar(stmt)
