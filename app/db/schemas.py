from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from app.db.models.user import UserRole


class UserBase(BaseModel):
    email: str
    nickname: str
    first_name: str | None
    last_name: str | None
    role: UserRole = UserRole.user

    class ConfigDict:
        use_enum_values = True


class User(UserBase):
    id: int
    is_active: bool

    class ConfigDict:
        from_atributes = True


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
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
    author_id: int
    group_id: int


class PostGet(PostDTO):
    id: int
    pub_date: datetime


class PostUpdate(BaseModel):
    text: Optional[str] = None
    group_id: Optional[int] = None


class CommentDTO(BaseModel):
    text: str
    author_id: int


class CommentUpdate(BaseModel):
    text: str


class CommentGet(CommentDTO):
    id: int
    created_at: datetime
    author: str
    post: int

    class ConfigDict:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    nickname: Optional[str] = None
