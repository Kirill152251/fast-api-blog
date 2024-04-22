import copy

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db import crud_group as crud
from app.db import schemas
from app.db.models import Group


def test_insert_group(db, first_group_dto):
    group = crud.create_group(db, first_group_dto)
    assert group != None
    group_from_db = db.scalars(select(Group)).all()
    assert len(group_from_db) == 1
    assert first_group_dto.slug == group_from_db[0].slug
    assert first_group_dto.description == group_from_db[0].description
    assert first_group_dto.title == group_from_db[0].title


def test_insert_group_with_already_used_slug(
    db,
    first_group_dto
):
    with pytest.raises(IntegrityError):
        crud.create_group(db, first_group_dto)
        crud.create_group(db, first_group_dto)
        group_from_db = db.scalars(select(Group)).all()
        assert len(group_from_db) == 1


def test_get_group_by_id(db, create_group_in_db):
    group = crud.get_group_by_id(db, create_group_in_db.id)
    assert to_dict(group) == to_dict(create_group_in_db)


def test_get_all_groups(db, create_several_groups_in_db):
    groups = copy.deepcopy(crud.get_groups(db))
    assert len(groups) == len(create_several_groups_in_db)
    for (a, b) in zip(groups, create_several_groups_in_db):
        assert to_dict(a) == to_dict(b)
    

def to_dict(group: Group): 
    return schemas.GroupGet.model_validate(
        group, from_attributes=True
    ).model_dump()

