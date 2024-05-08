from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey, String
from sqlalchemy import text as sqltext
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload, Session

from app.db import constants
from app.db.models.base import Base


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    pub_date: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=sqltext('CURRENT_TIMESTAMP')
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id'),
        nullable=False
    )

    author: Mapped['User'] = relationship('User', back_populates='posts')
    category: Mapped['Category'] = relationship('Category', back_populates='posts')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='post')


    @classmethod
    def find(cls, session: Session, where_conditions: list[Any]):
        stmt = (
            select(cls)
            .options(joinedload(cls.author, cls.category))
            .where(*where_conditions)
        )
        result = session.execute(stmt)
        return result.scalars().first()


    def __repr__(self):
        return f'Post(id={self.id}, text={self.text[:10]})'

