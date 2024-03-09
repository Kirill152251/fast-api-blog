from sqlalchemy.orm import Session
from sqlalchemy import update

from db import schemas
from db.models import User


def create_user(db: Session, user: schemas.UserCreate) -> User:
    user_dict = user.model_dump()
    hashed_password = user_dict.pop('password') + 'fakehash'
    db_user = User(
        **user_dict,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
    stmt = update(User).where(User.id==user_id).values(**user_data)
    db.execute(statement=stmt)
    db.commit()
    return db.get(User, user_id)