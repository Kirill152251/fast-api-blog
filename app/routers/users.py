from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import crud, schemas
from app.dependencies import get_db

router = APIRouter(tags=['users'])


@router.post('/users/', response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered'
        )
    return crud.create_user(db, user)


@router.get('/users/{user_id}/', response_model=schemas.User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
): 
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return db_user
    

@router.delete('/users/{user_id}/')
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    if not crud.delete_user(user_id=user_id, db=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return schemas.Message(message="User deleted successfully")


@router.put('/users/{user_id}/', response_model=schemas.User)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    user = crud.update_user(db, user_id, user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user
