from typing import Annotated, Union
from datetime import datetime

from pydantic import BaseModel

from db.models import UserRole


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    pub_date: datetime
    author_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    first_name: str | None
    last_name: str | None
    role: UserRole = UserRole.user


class User(UserBase):
    id: int
    is_active: bool
    # comments: list[Comment] = []

    class Config:
        from_atributes = True


class UserCreate(UserBase):
    password: str