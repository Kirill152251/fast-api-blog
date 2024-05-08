from typing import Any
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from app.db import constants
from app.db.models.base import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(constants.CATEGORY_TITLE_MAX_LEN),
        nullable=False
    )
    slug: Mapped[str] = mapped_column(
        String(constants.CATEGORY_SLUG_MAX_LEN),
        nullable=False,
        unique=True,
    )
    description: Mapped[str | None]

    posts: Mapped[list['Post']] = relationship('Post', back_populates='category')


    @classmethod
    def find(cls, session: Session, where_conditions: list[Any]):
        stmt = select(cls).where(*where_conditions)
        result = session.execute(stmt)
        return result.scalars().first()
    

    def __repr__(self):
        return f'Category(id={self.id}, slug={self.slug})'

