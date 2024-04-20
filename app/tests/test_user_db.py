from copy import deepcopy
import pytest
from fastapi import status

from sqlalchemy.orm import Session

from app.db.models import User
from app.db import schemas
from app.db import crud_user


def test_create_user(user_create_dict: dict, db: Session):
    user = crud_user.create_user(db, schemas.UserCreate(**user_create_dict))
    assert user != None 
    assert user.email == user_create_dict['email']
    assert user.role == user_create_dict['role']

