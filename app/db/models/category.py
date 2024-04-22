from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import constants
from app.db.models import Base


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


    @classmethod
    def find(cls, session: Session, where_conditions: list[Any]):
        _stmt = select(cls).where(*where_conditions)
        _result = session.execute(_stmt)
        return _result.scalars().first()
    

    def __repr__(self):
        return f'Category(id={self.id}, slug={self.slug})'

