from sqlalchemy.orm import Session
from sqlalchemy import update, insert, select, delete

from app.db import schemas
from app.db.models import User, Group, Post


def create_user(db: Session, user: schemas.UserCreate) -> User:
    user_dict = user.model_dump()
    hashed_password = user_dict.pop('password') + 'fakehash'
    user_dict['hashed_password'] = hashed_password
    user = db.scalar(
        insert(User).returning(User),
        user_dict
    )
    db.commit()
    return user


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def update_user(
    db: Session,
    user_id: int,
    user_in: schemas.UserUpdate
) -> User | None:
    db_user = db.get(User, user_id)
    if not db_user:
        return None
    user_data = user_in.model_dump(exclude_unset=True)
    user = db.scalar(
        update(User)
        .returning(User)
        .where(User.id==user_id).values(**user_data)
    )
    db.commit()
    return user


def get_groups(db: Session) -> list[Group]:
    result = db.scalars(
        select(Group).order_by(Group.id)
    ).all()
    return result


def get_group_by_id(db: Session, group_id: int) -> Group | None:
    return db.get(Group, group_id)


def create_group(
    db: Session,
    group: schemas.GroupDTO
) -> Group:
    db_group = db.scalar(
        insert(Group).returning(Group),
        group.model_dump()
    )
    db.commit()
    return db_group

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
        select(Group).order_by(Group.id)
    ).all()
    return posts

def delete_post(db: Session, post_id) -> Post | None:
    post = db.scalar(
        delete(Post).where(Post.id == post_id).returning(Post)
    )
    db.commit()
    return post