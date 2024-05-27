from typing import Annotated
from datetime import timedelta, datetime, timezone

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt

from app.config import settings
from app.db import schemas
from app.db.models.user import User, UserRole
from app.dependencies import get_db


SECRET_KEY = str(settings.JWT_SECRET)
ALGORITHM = str(settings.JWT_ALG)
TOKEN_EXPIRE_MIN = int(settings.JWT_EXP_MIN) 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MIN)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_db)    
) -> User:
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    try:
        paylaod = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nickname: str = paylaod.get('sub')
        if nickname is None:
            raise credentials_exception
        token_data = schemas.TokenData(nickname=nickname)
    except JWSError:
        raise credentials_exception
    user: User = User.find(session, [User.nickname == token_data.nickname]) 
    if user is None:
        raise credentials_exception
    return user


async def get_admin(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if current_user.role == UserRole.admin:
        return current_user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

