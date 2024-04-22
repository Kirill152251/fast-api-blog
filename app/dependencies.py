from typing import Annotated, Mapping

from fastapi import Depends, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Group
from app.db.schemas import GroupDTO


pwd_context = CryptContext(schemes=['bcrypt'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]


def validate_group_create(group_in: GroupDTO) -> Mapping:
    slug = group_in.slug
    is_used = session.query(Group.id).filter_by(slug=slug).first()
    if is_used: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Slug is already used.'
        )
    return group_in 


def valid_group_slug(slug: str) -> Mapping:
    is_exist = session.query(Group.id).filter_by(slug=slug).first()
    if not is_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Group not found'
        )
    return slug



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)
