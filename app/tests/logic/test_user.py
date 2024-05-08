import pytest
from fastapi import status
from fastapi.testclient import TestClient

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from app.db.models.user import User 
from app.db import schemas
from app.db import crud_user
from app.tests.logic.conftest import auth_user 


def test_create_user_with_valid_data(
    user_schema: schemas.UserCreate,
    client: TestClient 
):
    response = client.post(
        '/users/',
        json=user_schema.model_dump()
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['email'] == user_schema.email 
    assert data['nickname'] == user_schema.nickname 
    assert data['first_name'] == user_schema.first_name
    assert data['last_name'] == user_schema.last_name
    assert data['role'] == user_schema.role
    assert 'id' in data


def test_user_me_get(client: TestClient):
    response = client.get(
        '/users/me/'
    )
    assert response.status_code == status.HTTP_200_OK 
    data = response.json()
    assert data['email'] == auth_user.email 
    assert data['nickname'] == auth_user.nickname 
    assert data['first_name'] == auth_user.first_name
    assert data['last_name'] == auth_user.last_name
    assert data['role'] == auth_user.role


def test_user_me_post(client: TestClient):
    new_data = schemas.UserUpdate(
        nickname='new_nick_name',
        last_name='new_last_name',
        first_name='new_f_n',
        email='new@gmail.com'
    )
    response = client.put(
        '/users/me/',
        json=new_data.model_dump(exclude_unset=True)
    )
    assert response.status_code == status.HTTP_200_OK 
    data = response.json()
    assert data['email'] == new_data.email 
    assert data['nickname'] == new_data.nickname 
    assert data['first_name'] == new_data.first_name
    assert data['last_name'] == new_data.last_name


def test_user_me_post_only_one_field(client: TestClient):
    new_data = schemas.UserUpdate(
        nickname='new_nick_name',
    )
    response = client.put(
        '/users/me/',
        json=new_data.model_dump(exclude_unset=True)
    )
    assert response.status_code == status.HTTP_200_OK 
    data = response.json()
    assert data['nickname'] == new_data.nickname 


@pytest.mark.usefixtures('save_user')
@pytest.mark.usefixtures('save_admin')
def test_users_get(client: TestClient):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK 
    data = response.json()
    assert len(data) == 3 # two with fixtures and one with overrided get_admin dep


def test_user_get(client: TestClient, save_user: User):
    response = client.get(f'/users/{save_user.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['nickname'] == save_user.nickname


def test_delete_user(client: TestClient, save_user: User, db):
    response = client.delete(f'/users/{save_user.id}')
    assert response.status_code == status.HTTP_200_OK
    user = User.find(db, [User.id==save_user.id])
    assert user == None
