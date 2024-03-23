import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import User, Base
from app.main import app
from app.db import crud_post, crud_group, schemas, models
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
    return schemas.User.model_validate(
        user_saved_to_db, from_attributes=True
    ).model_dump()

@pytest.fixture
def put_user_dict():
    return {
        "email": "newemail@mail.com",
        "first_name": "newkirill",
        "last_name": "newermalenok",
    }

@pytest.fixture
def first_group_dto():
    return schemas.GroupDTO(
        title='test title',
        slug='travel',
        description='some description'
    )

@pytest.fixture
def second_group_dto():
    return schemas.GroupDTO(
        title='test title two',
        slug='travel2',
        description='some description'    
    )

@pytest.fixture
def create_group_in_db(db, first_group_dto):
    return crud_group.create_group(db, first_group_dto)

@pytest.fixture
def create_several_groups_in_db(db, create_group_in_db, second_group_dto):
    groups = []
    groups.append(create_group_in_db)
    groups.append(crud_group.create_group(db, second_group_dto))
    return sorted(groups, key=lambda group: group.id)

@pytest.fixture
def post_dto(
    user_saved_to_db: models.User,
    create_group_in_db: models.Group
):
    return schemas.PostDTO(
        text='post text',
        author_id=user_saved_to_db.id,
        group_id=create_group_in_db.id
    )

@pytest.fixture
def create_post_in_db(db, post_dto):
    return crud_post.create_post(db, post_dto)

@pytest.fixture
def create_two_posts(
    db,
    user_saved_to_db: models.User,
    create_group_in_db: models.Group
):
    posts = []
    posts.append(
        crud_post.create_post(
            db,
            schemas.PostDTO(
                text='post text',
                author_id=user_saved_to_db.id,
                group_id=create_group_in_db.id
            )
        )
    )
    posts.append(
        crud_post.create_post(
            db,
            schemas.PostDTO(
                text='second post text',
                author_id=user_saved_to_db.id,
                group_id=create_group_in_db.id
            )
        )
    )
    return posts

@pytest.fixture
def post_update_full(
    create_several_groups_in_db,
):
    return schemas.PostUpdate(
        text='afaljfajf;ka',
        group_id=create_several_groups_in_db[1].id
    )

@pytest.fixture
def post_update_text():
    return schemas.PostUpdate(
        text='fakjgoiabja'
    )

@pytest.fixture
def post_update_group_id(create_several_groups_in_db):
    return schemas.PostUpdate(
        group_id=create_several_groups_in_db[1].id
    )
