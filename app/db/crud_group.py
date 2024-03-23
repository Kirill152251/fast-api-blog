from sqlalchemy.orm import Session
from sqlalchemy import insert, select

from app.db import schemas
from app.db.models import Group

def get_groups(db: Session) -> list[Group]:
    result = db.scalars(
        select(Group).order_by(Group.id)
    ).all()
    return result


def get_group_by_id(db: Session, group_id: int) -> Group | None:
    return db.get(Group, group_id)


def create_group(
    db: Session,
    group: schemas.GroupDTO
) -> Group:
    db_group = db.scalar(
        insert(Group).returning(Group),
        group.model_dump()
    )
    db.commit()
    return db_group