from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db import crud_user, schemas, models
from app.db.utils import is_exist
from app.dependencies import get_db
from app.auth import get_current_user, get_admin

router = APIRouter(tags=['users'])

@router.get('/users/me', response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    """Get your profile details. Access rights: any authorized user."""
    return current_user


@router.put('/users/me', response_model=schemas.User)
async def update_user_me(
    updated_data: schemas.UserUpdate,
    current_user: Annotated[schemas.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Update your profile details. Access rights: any authorized user."""
    return crud_user.update_user(db, current_user.id, updated_data)


@router.post(
    '/users/',
    response_model=schemas.User,
    dependencies=[Depends(get_admin)]
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Create new user. Email must be unique. Access rights: admin."""
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered.'
        )
    return crud_user.create_user(db, user)


@router.get(
    '/users/',
    response_model = List[schemas.User],
    dependencies=[Depends(get_admin)]
)
def get_users(
    db: Session = Depends(get_db),
    first_name: Annotated[
        str | None,
        Query(description='Search by first name')
    ] = None,
    last_name: Annotated[
        str | None,
        Query(description='Search by last name')
    ] = None
):
    """Get all users, ordered by id. Access rights: admin."""
    return crud_user.get_all_users(db, first_name, last_name)


@router.get(
    '/users/{user_id}/',
    response_model=schemas.User,
    dependencies=[Depends(get_admin)]
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by user id. Access rights: admin"""
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return db_user
    

@router.delete(
    '/users/{user_id}/',
    response_model=schemas.Message,
    dependencies=[Depends(get_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete user by id. Access rights: admin."""
    if not crud_user.delete_user(user_id=user_id, db=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return schemas.Message(message="User deleted successfully")


@router.put(
    'users/{user_id}/',
    response_model=schemas.User,
    dependencies=[Depends(get_admin)]
)
def update_user(
    user_id: int,
    updated_data: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    """Update user by id. Access rights: admin"""
    if not is_exist(db, user_id, models.User):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return crud_user.update_user(db, user_id, updated_data)
