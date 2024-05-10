import pytest
from pytest_lazy_fixtures import lf
from fastapi import status
from fastapi.testclient import TestClient

from app.db import schemas
from app.db.models.user import User


@pytest.mark.parametrize(
    'headers, expected',
    [
        (lf('auth_user_headers'), status.HTTP_200_OK),
        (None, status.HTTP_401_UNAUTHORIZED)
    ]
)
def test_users_me_get(client, headers, expected):
    response = client.get('/users/me', headers=headers)
    assert response.status_code == expected


@pytest.mark.parametrize(
    'headers, expected',
    [
        (lf('auth_user_headers'), status.HTTP_200_OK),
        (None, status.HTTP_401_UNAUTHORIZED)
    ]
)
def test_users_me_put(client, headers, expected):
    new_data = schemas.UserUpdate(
        first_name='first_name_new',
    )
    response = client.put(
        '/users/me',
        json=new_data.model_dump(exclude_unset=True),
        headers=headers
    )
    assert response.status_code == expected


@pytest.mark.parametrize(
    'headers, expected',
    [
        (None, status.HTTP_401_UNAUTHORIZED),
        (lf('auth_user_headers'), status.HTTP_401_UNAUTHORIZED),
        (lf('auth_admin_headers'), status.HTTP_201_CREATED)
    ]
)
def test_user_post(client, headers, expected, rnd_user_create_schema):
    response = client.post(
        '/users',
        json=rnd_user_create_schema.model_dump(exclude_unset=True),
        headers=headers
    )
    assert response.status_code == expected


@pytest.mark.parametrize(
    'headers, expected',
    [
        (None, status.HTTP_401_UNAUTHORIZED),
        (lf('auth_user_headers'), status.HTTP_401_UNAUTHORIZED),
        (lf('auth_admin_headers'), status.HTTP_200_OK)
    ]
)
def test_users_get(client, headers, expected):
    response = client.get(
        '/users',
        headers=headers
    )
    assert response.status_code == expected


@pytest.mark.parametrize(
    'headers, expected',
    [
        (None, status.HTTP_401_UNAUTHORIZED),
        (lf('auth_user_headers'), status.HTTP_401_UNAUTHORIZED),
        (lf('auth_admin_headers'), status.HTTP_200_OK)
    ]
)
def test_user_get(client, db, headers, expected, rnd_user_create_schema):
    user = User(**rnd_user_create_schema.model_dump())
    user.save(db)
    response = client.get(
        f'/users/{user.id}',
        headers=headers
    )
    assert response.status_code == expected


@pytest.mark.parametrize(
    'headers, expected',
    [
        (None, status.HTTP_401_UNAUTHORIZED),
        (lf('auth_user_headers'), status.HTTP_401_UNAUTHORIZED),
        (lf('auth_admin_headers'), status.HTTP_200_OK)
    ]
)
def test_user_delete(client, db, headers, expected, rnd_user_create_schema):
    user = User(**rnd_user_create_schema.model_dump())
    user.save(db)
    response = client.delete(
        f'/users/{user.id}',
        headers=headers
    )
    assert response.status_code == expected


@pytest.mark.parametrize(
    'headers, expected',
    [
        (None, status.HTTP_401_UNAUTHORIZED),
        (lf('auth_user_headers'), status.HTTP_401_UNAUTHORIZED),
        (lf('auth_admin_headers'), status.HTTP_200_OK)
    ]
)
def test_user_put(client, db, headers, expected, rnd_user_create_schema):
    user = User(**rnd_user_create_schema.model_dump())
    user.save(db)
    new_data = schemas.UserUpdate(
        first_name='first_name_new',
    )
    response = client.put(
        f'/users/{user.id}',
        json=new_data.model_dump(exclude_unset=True),
        headers=headers
    )
    assert response.status_code == expected

