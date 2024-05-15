from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey, select
from sqlalchemy import text as sqltext
from sqlalchemy.orm import Mapped, joinedload, mapped_column, Session, relationship
from app.db.models.base import Base


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=sqltext("TIMEZONE('utc', now())")
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', name='comment_author'),
        nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id', name='related_post'),
        nullable=False
    )

    author: Mapped['User'] = relationship(back_populates='comments')
    post: Mapped['Post'] = relationship(back_populates='comments')


    @classmethod
    def find(cls, session: Session, where_conditions: list[Any]):
        stmt = (
            select(cls)
            .options(joinedload(cls.author, cls.post))
            .where(*where_conditions)
        )
        result = session.execute(stmt)
        return result.scalars().first()


    def __repr__(self):
        return f'Comment(id={self.id}, text={self.text[:10]})'
