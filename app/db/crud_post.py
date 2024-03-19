from sqlalchemy.orm import Session
from sqlalchemy import update, insert, select, delete

from app.db import schemas
from app.db.models import User, Group, Post

def create_post(
    db: Session,
    post: schemas.PostDTO
) -> Post | None:
    author = db.get(User, post.author_id)
    group = db.get(Group, post.group_id)
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
    db.commit()
    return post

def update_post(db: Session, ):
    pass