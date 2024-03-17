import enum
import re
from datetime import datetime
from typing import List

from sqlalchemy import (
    Boolean, Column, 
    ForeignKey, Integer, 
    String, Enum
)
from sqlalchemy import text as sqltext
from sqlalchemy.orm import relationship, mapped_column, Mapped, validates, declarative_base

from app.db import constants

Base = declarative_base()


class UserRole(str, enum.Enum):
    user = 'user'
    admin = 'admin'
    superuser = 'superuser'


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(constants.GROUP_TITLT_MAX_LEN),
        nullable=False
    )
    slug: Mapped[str] = mapped_column(
        String(constants.GROUP_SLUG_MAX_LEN),
        nullable=False,
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        nullable= False
    )

    posts: Mapped[List['Post']] = relationship(back_populates='group')


    @validates('slug')
    def validate_slug(self, key, slug):
        if not re.match(constants.SLUG_REGEX_PATT, slug):
            raise ValueError(
                'Slug field should match ' 
                f'regex pattern {constants.SLUG_REGEX_PATT}'
            )
        return slug
    
    def __repr__(self):
        return f'group: id={self.id}, slug={self.slug}'
    

class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.user)

    comments: Mapped[List['Comment']] = relationship(back_populates='author')
    posts: Mapped[List['Post']] = relationship(back_populates='author')


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=sqltext("DATE('now')")
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )

    author: Mapped['User'] = relationship(back_populates='comments')

    def __repr__(self):
        return f'comment: id={self.id}, text={self.text[:10]}'


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    pub_date: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=sqltext("DATE('now')")
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey('groups.id'),
        nullable=False
    )

    author: Mapped['User'] = relationship(back_populates='posts')
    group: Mapped['Group'] = relationship(back_populates='posts')

    def __repr__(self):
        return f'post: id={self.id}, text={self.text[:10]}'
