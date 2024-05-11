import pytest
from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.models.base import Base
from app.db.models.user import User
from main import app
from app.db import schemas
from app.dependencies import get_db


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:cooldb@localhost:5432/test_blog'
engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
PASSWORD = 'secret_key'

auth_admin = schemas.UserCreate(
    nickname='fsdfa',
    email='admin19571@mail.com',
    first_name='faf',
    last_name='jkja',
    password=PASSWORD,
    role='admin'
)

auth_user = schemas.UserCreate(
    nickname='fallfsdfa',
    email='user616840@mail.com',
    first_name='faf',
    last_name='jkja',
    password=PASSWORD,
    role='user'
)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_admin(db: Session = Depends(get_db)):
    user = User.find(db, [User.email==auth_admin.email])
    if not user:
        user = User(**auth_admin.model_dump())
        user.save(db)
    return user


def override_get_current_user(db: Session = Depends(get_db)):
    user = User.find(db, [User.email==auth_user.email])
    if not user:
        user = User(**auth_user.model_dump())
        user.save(db)
    return user


app.dependency_overrides[get_db] = override_get_db
user_client = TestClient(app)


@pytest.fixture(scope='session')
def client():
    return user_client


@pytest.fixture(autouse=True)
def db():
    Base.metadata.create_all(bind=engine)
    db_session_local = TestingSessionLocal()
    yield db_session_local
    db_session_local.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def admin_schema():
    return schemas.UserCreate(
        nickname='Jackpot',
        email='email@mail.com',
        first_name='Kirill',
        last_name='Ermalenok',
        password=PASSWORD,
        role='admin'
    )


@pytest.fixture
def user_schema():
    return schemas.UserCreate(
        nickname='Jackpot1',
        email='email1@mail.com',
        first_name='Kirill',
        last_name='Ermalenok',
        password=PASSWORD,
        role='user'
    )


@pytest.fixture
def save_admin(admin_schema, db):
    user = User(**admin_schema.model_dump())
    user.save(db)
    return user


@pytest.fixture
def save_user(user_schema, db):
    user = User(**user_schema.model_dump())
    user.save(db)
    return user

