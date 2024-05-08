from fastapi import Depends
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql.functions import user

from app.db.models.base import Base
from app.db.models.user import User
from main import app
from app.db import schemas, models
from app.dependencies import get_db
from app.auth import get_current_user, get_admin


SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
PASSWORD = 'secret_key'

auth_admin = schemas.UserCreate(
    nickname='fsdfa',
    email='admin@mail.com',
    first_name='faf',
    last_name='jkja',
    password=PASSWORD,
    role='admin'
)

auth_user = schemas.UserCreate(
    nickname='fallfsdfa',
    email='user@mail.com',
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
    user = User(**auth_admin.model_dump())
    user.save(db)
    return user


def override_get_current_user(db: Session = Depends(get_db)):
    user = User(**auth_user.model_dump())
    user.save(db)
    return user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_admin] = override_get_admin
app.dependency_overrides[get_current_user] = override_get_current_user
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

