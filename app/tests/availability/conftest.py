from random import randint

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models.base import Base
from app.db.models.user import User
from app.db import schemas
from app.dependencies import get_db 
from main import app


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:cooldb@localhost:5432/test_blog'
engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
PASSWORD = 'secret_key'


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
user_client = TestClient(app)


@pytest.fixture(scope='session')
def client():
    return user_client


@pytest.fixture(scope='module', autouse=True)
def db():
    Base.metadata.create_all(bind=engine)
    db_session_local = TestingSessionLocal()
    yield db_session_local
    db_session_local.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def rnd_user_create_schema():
    return schemas.UserCreate(
        nickname=f'Jackpot{str(randint(0, 100000))}',
        email=f'email{str(randint(0, 100000))}@mail.com',
        first_name='Kirill',
        last_name='Ermalenok',
        password=PASSWORD,
        role='user'
    )


@pytest.fixture(scope='module')
def auth_user_headers(client, db):
    user_schema = schemas.UserCreate(
        nickname='Jackpot',
        email='email@mail.com',
        first_name='Kirill',
        last_name='Ermalenok',
        password=PASSWORD,
        role='user'
    )
    user = User(**user_schema.model_dump())
    user.save(db)
    data = {'username': user_schema.nickname, 'password': user_schema.password }
    response = client.post('/token', data=data)
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope='module')
def auth_admin_headers(client, db):
    user_schema = schemas.UserCreate(
        nickname='Jackpot1',
        email='email1@mail.com',
        first_name='Kirill',
        last_name='Ermalenok',
        password=PASSWORD,
        role='admin'
    )
    user = User(**user_schema.model_dump())
    user.save(db)
    data = {'username': user_schema.nickname, 'password': user_schema.password }
    response = client.post('/token', data=data)
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}

