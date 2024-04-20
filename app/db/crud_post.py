from sqlalchemy.orm import Session
from sqlalchemy import update, insert, select, delete

from app.db import schemas
from app.db.models import User, Group, Post
from app.db.utils import is_exist

def create_post(
    db: Session,
    post: schemas.PostDTO
) -> Post | None:
    author = is_exist(db, post.author_id, User)
    group = is_exist(db, post.group_id, Group)
    if not author or not group:
        return None
    db_post = db.scalar(
        insert(Post).returning(Post),
        post.model_dump()
    )
    return db_post

def get_post_by_id(
    db: Session,
    post_id: int
) -> Post | None:
    return db.get(Post, post_id)

def get_all_posts(db: Session) -> list[Post]:
    posts = db.scalars(
        select(Post).order_by(Post.id)
    ).all()
    return posts

def delete_post(db: Session, post_id) -> Post | None:
    post = db.scalar(
        delete(Post).where(Post.id == post_id).returning(Post)
    )
    return post

def update_post(
    db: Session,
    post_id: int,
    new_post_data: schemas.PostUpdate
) -> Post | None:
    if new_post_data.group_id != None:
        is_group_exist = is_exist(db, new_post_data.group_id, Group)
        if not is_group_exist:
            return None
    new_data_dict = new_post_data.model_dump(exclude_unset=True)
    stmt = (
        update(Post)
        .where(Post.id==post_id)
        .values(**new_data_dict)
        .returning(Post)
    )
    return db.scalar(stmt)
