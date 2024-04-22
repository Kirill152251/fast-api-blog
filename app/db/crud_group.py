from sqlalchemy.orm import Session
from sqlalchemy import delete, insert, select

from app.db import schemas
from app.db.models import Group
from app.db.utils import is_exist


def get_groups(db: Session, limit: int, offset: int) -> list[Group]:
    groups = db.scalars(
        select(Group).limit(limit).offset(offset).order_by(Group.id)
    ).all()
    return groups 


def get_group_by_id(db: Session, group_id: int) -> Group | None:
    return db.get(Group, group_id)


def create_group(
    db: Session,
    group: schemas.GroupDTO
) -> Group | None:
    db_group = db.scalar(
        insert(Group).returning(Group),
        group.model_dump()
    )
    return db_group


def delete_group_by_slug(db: Session, slug: str) -> Group | None:
    exist = db.query(Group.id).filter_by(slug=slug).first() is not None
    if not exist:
        return None
    group = db.scalar(
        delete(Group).where(Group.slug == slug).returning(Group)
    )
    return group

