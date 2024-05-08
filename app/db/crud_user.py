from sqlalchemy.orm import Session
from sqlalchemy import update, insert, select

from app.db import schemas
from app.db.models.user import User


def create_user(db: Session, user: schemas.UserCreate) -> User:
    user_dict = user.model_dump()
    hashed_password = get_hashed_password(user_dict.pop('password'))
    user_dict['hashed_password'] = hashed_password
    user = db.scalar(
        insert(User).returning(User),
        user_dict
    )
    db.commit()
    return user


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_all_users(
    db: Session,
    first_name: str | None = None,
    last_name: str | None = None
) -> list[User]:
    if first_name and last_name:
        stmt = select(User).where(
            User.first_name == first_name,
            User.last_name == last_name
        )
    elif first_name:
        stmt = select(User).where(
            User.first_name == first_name,
        )
    elif last_name:
        stmt = select(User).where(
            User.last_name == last_name,
        )
    else:
        stmt = select(User)
    return db.execute(stmt.order_by(User.id)).scalars().all()


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
        .where(User.id == user_id).values(**user_data)
    )
    db.commit()
    return user
