from sqlalchemy.orm import Session

from db import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    user_dict = user.model_dump()
    hashed_password = user_dict.pop('password') + 'fakehash'
    db_user = models.User(
        **user_dict,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()
