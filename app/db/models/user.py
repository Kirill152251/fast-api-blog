import enum
from typing import Any

from passlib.context import CryptContext
from sqlalchemy import Boolean, Enum, Integer, String, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from app.db.models.base import Base


pwd_context = CryptContext(schemes=['bcrypt'])


class UserRole(str, enum.Enum):
    user = 'user'
    admin = 'admin'
    superuser = 'superuser'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    _password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)

    comments: Mapped[list['Comment']] = relationship(back_populates='author')
    posts: Mapped[list['Post']] = relationship(back_populates='author')


    @property
    def password(self):
        return self._password


    @password.setter
    def password(self, password: str):
        self._password = pwd_context.hash(password)


    def check_password(self, password: str):
        return pwd_context.verify(password, self.password)


    @classmethod
    def find(cls, session: Session, where_conditions: list[Any]):
        _stmt = select(cls).where(*where_conditions)
        _result = session.execute(_stmt)
        return _result.scalars().first()


    @classmethod
    def find_all(cls, session: Session, where_conditions: list[Any] = []):
        _stmt = select(cls).where(*where_conditions)
        _result = session.execute(_stmt.order_by(cls.id))
        return _result.scalars().all()


    def __repr__(self):
        return f'User(id={self.id}, email={self.nickname})'

