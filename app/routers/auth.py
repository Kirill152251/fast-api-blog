from datetime import timedelta
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import authenticate_user, TOKEN_EXPIRE_MIN, create_access_token
from app.db.schemas import Token
from app.dependencies import get_db


router = APIRouter(tags=['auth'])

@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MIN)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')
    