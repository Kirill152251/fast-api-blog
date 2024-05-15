from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db import crud_user, schemas, models
from app.db.models.user import User
from app.db.utils import is_exist
from app.dependencies import get_db
from app.auth import get_current_user, get_admin


router = APIRouter(tags=['users'])


@router.get('/users/me', response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Get your profile details. Access rights: any authorized user."""
    return current_user


@router.put('/users/me', response_model=schemas.User)
async def update_user_me(
    updated_data: schemas.UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    """Update your profile details. Access rights: any authorized user."""
    current_user.update(session, **updated_data.model_dump(exclude_unset=True))
    return current_user


@router.post(
    '/users',
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_admin)]
)
def create_user(
    payload: schemas.UserCreate,
    session: Session = Depends(get_db)
):
    """Create new user. Email must be unique. Access rights: admin."""
    user: User = User(**payload.model_dump())
    user.save(session)
    return user 


@router.get(
    '/users',
    response_model = List[schemas.User],
    dependencies=[Depends(get_admin)]
)
def get_users(session: Session = Depends(get_db)):
    """Get all users, ordered by id. Access rights: admin."""
    return User.find_all(session)


@router.get(
    '/users/{user_id}',
    response_model=schemas.User,
    dependencies=[Depends(get_admin)]
)
def get_user(user_id: int, session: Session = Depends(get_db)):
    """Get user by user id. Access rights: admin"""
    user = User.find(session, [User.id==user_id])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user
    

@router.delete(
    '/users/{user_id}',
    response_model=schemas.Message,
    dependencies=[Depends(get_admin)]
)
def delete_user(user_id: int, session: Session = Depends(get_db)):
    """Delete user by id. Access rights: admin."""
    user = User.find(session, [User.id==user_id])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    user.delete(session)
    return schemas.Message(message="User deleted successfully")


@router.put(
    '/users/{user_id}',
    response_model=schemas.User,
    dependencies=[Depends(get_admin)]
)
def update_user(
    user_id: int,
    updated_data: schemas.UserUpdate,
    session: Session = Depends(get_db)
):
    """Update user by id. Access rights: admin"""
    user = User.find(session, [User.id==user_id])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    user.update(session, **updated_data.model_dump(exclude_unset=True))
    return user

