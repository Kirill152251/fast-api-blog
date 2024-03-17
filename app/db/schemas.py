from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from app.db.models import UserRole


class UserBase(BaseModel):
    email: str
    first_name: str | None
    last_name: str | None
    role: UserRole = UserRole.user

    class ConfigDict:
        use_enum_values = True


class User(UserBase):
    id: int
    is_active: bool
    # comments: list[Comment] = []

    class ConfigDict:
        from_atributes = True


class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class Message(BaseModel):
    message: str


class GroupDTO(BaseModel):
    title: str
    slug: str
    description: str


class GroupGet(GroupDTO):
    id: int


class PostDTO(BaseModel):
    text: str
    author: str
    group: int


class PostGet(PostDTO):
    id: str
    pub_date: datetime


class CommentDTO(BaseModel):
    text: str


class CommentGet(CommentDTO):
    id: int
    created_at: datetime
    author: str
    post: int

    class ConfigDict:
        from_attributes = True
