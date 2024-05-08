import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql.functions import user

from app.db.models.base import Base
from app.db.models.user import User
from main import app
from app.db import schemas, models
from app.dependencies import get_db 


SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
)
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
def clear_db(db):
    db.execute(delete(User))


@pytest.fixture(scope='module')
def admin_schema():
    return schemas.UserCreate(
        nickname='Jackpot',
        email='email@mail.com',
        first_name='Kirill',
        last_name='Ermalenok',
        password=PASSWORD,
        role='admin'
    )


@pytest.fixture(scope='module')
def user_schema():
    return schemas.UserCreate(
        nickname='Jackpot1',
        email='email1@mail.com',
        first_name='Kirill',
        last_name='Ermalenok',
        password=PASSWORD,
        role='user'
    )


@pytest.fixture(scope='module')
def save_admin(admin_schema, db):
    user = User(**admin_schema.model_dump())
    user.save(db)
    return user


@pytest.fixture(scope='module')
def save_user(user_schema, db):
    user = User(**user_schema.model_dump())
    user.save(db)
    return user


@pytest.fixture(scope='module')
def auth_user_headers(
    client: TestClient,
    user_schema: schemas.UserCreate,
    save_user: User
):
    data = {'username': user_schema.nickname, 'password': user_schema.password }
    response = client.post('/token', data=data)
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope='module')
def auth_admin_headers(
    client: TestClient,
    admin_schema: schemas.UserCreate,
    save_admin: User
):
    data = {'username': admin_schema.nickname, 'password': admin_schema.password }
    response = client.post('/token', data=data)
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}

