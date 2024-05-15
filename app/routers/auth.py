from datetime import timedelta
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import TOKEN_EXPIRE_MIN, create_access_token
from app.db.models.user import User
from app.db.schemas import Token
from app.dependencies import get_db


router = APIRouter(tags=['auth'])

@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_db)
) -> Token:
    user: User = User.find(session, [User.nickname == form_data.username])
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MIN)
    access_token = create_access_token(
        data={'sub': user.nickname}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')

    
