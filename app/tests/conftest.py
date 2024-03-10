import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base
from app.db.models import User
from app.main import app
from app.dependencies import get_db


SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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

@pytest.fixture(scope='function', autouse=True)
def db():
    Base.metadata.create_all(bind=engine)
    db_session_local = TestingSessionLocal()
    yield db_session_local
    db_session_local.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def user_create_dict():
    return {
        "email": "email@mail.com",
        "first_name": "kirill",
        "last_name": "ermalenok",
        "password": "password",
        "role": "admin"
    }

@pytest.fixture
def db_user_create_dict(user_create_dict):
    db_create_dict = user_create_dict.copy()
    db_create_dict.pop('password')
    db_create_dict['hashed_password'] = 'passwordfake'
    return db_create_dict

@pytest.fixture
def user_saved_to_db(db, db_user_create_dict):
    db_user = User(**db_user_create_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@pytest.fixture
def response_user_dict(user_saved_to_db):
    user_dict = user_saved_to_db.__dict__
    user_dict.pop('_sa_instance_state')
    user_dict.pop('hashed_password')
    user_dict['role'] = 'admin'
    return user_dict

@pytest.fixture
def put_user_dict():
    return {
        "email": "newemail@mail.com",
        "first_name": "newkirill",
        "last_name": "newermalenok",
    }

