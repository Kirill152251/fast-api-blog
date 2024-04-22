from typing import Annotated, Any, Mapping 

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db import crud_group, schemas, models
from app.db.utils import is_exist
from app.dependencies import SessionDep, validate_group_create
from app.auth import get_current_user, get_admin


router = APIRouter(tags=['groups'])


@router.get(
    '/groups/',
    response_model=list[schemas.GroupGet]
)
def get_all_groups(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """Get all groups. Access rights: anyone."""
    groups = crud_group.get_groups(session, limit, skip)
    return groups 


@router.post(
    '/groups/',
    response_model=schemas.GroupDTO,
    dependencies=[Depends(get_admin)]
)
def post_group(
    session: SessionDep,
    group_in: Mapping = Depends(validate_group_create) 
) -> Any:
    """Create group. Slug should be unique. Access right: admin."""
    return crud_group.create_group(session, group_in)


@router.delete(
    '/groups/{slug}/',
    response_model=schemas.GroupDTO,
    dependencies=[Depends(get_admin)]
)
def delete_group_by_slug(
    session: SessionDep,
    slug: str
) -> Any:
    """Delete group by slug. Access right: admin."""
    group = crud_group.delete_group_by_slug(db, slug) 
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return group

