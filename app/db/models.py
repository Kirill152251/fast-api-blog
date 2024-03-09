import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from app.db.database import Base


class UserRole(enum.Enum):
    user = 'user'
    admin = 'admin'
    superuser = 'superuser'


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.user)

    comments = relationship('Comment', back_populates='author')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column('id', Integer, primary_key=True)
    text = Column(String)
    pub_date = Column(DateTime)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', back_populates='comments')
