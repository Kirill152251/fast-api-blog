import pytest
from fastapi import status


def test_user_create(client, user_create_dict):
    response = client.post('/users/', json=user_create_dict)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['email'] == user_create_dict['email']
    assert data['first_name'] == user_create_dict['first_name']
    assert data['last_name'] == user_create_dict['last_name']
    assert data['role'] == user_create_dict['role']
    assert 'id' in data


@pytest.mark.usefixtures('user_saved_to_db')
def test_cannot_create_user_with_already_used_email(
    client,
    user_create_dict
):
    response = client.post('/users/', json=user_create_dict)
    assert response.status_code == 400


@pytest.mark.usefixtures('user_saved_to_db')
def test_login(client, current_user):
    response = client.post(
        '/token',
        data=current_user
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()['access_token']
    token_type = response.json()['token_type']
    assert token is not None
    assert token_type == 'bearer'
    return token


@pytest.mark.usefixtures('user_saved_to_db')
def test_users_me(client, current_user):
    token = test_login(client, current_user)
    response = client.get(
        '/users/me',
        headers={"Authorization": f"Bearer {token}"}
    )
    print(response.json())
    assert current_user['username'] == response.json()['email']
    assert response.status_code == status.HTTP_200_OK


def test_users_me_for_anonymous_user(client):
    response = client.get('/users/me')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_user_by_id(client, response_user_dict):
    response = client.get(f'/users/{response_user_dict["id"]}')
    assert response.status_code == 200
    assert response.json() == response_user_dict


def test_get_non_exist_user(client, response_user_dict):
    response = client.get(f'/users/{response_user_dict["id"]+1}')
    assert response.status_code == 404


def test_delete_user(client, response_user_dict):
    response = client.delete(f'/users/{response_user_dict["id"]}')
    assert response.status_code == 200


def test_delete_non_exist_user(client, response_user_dict):
    response = client.delete(f'/users/{response_user_dict["id"]+1}')
    assert response.status_code == 404


def test_put_user(client, response_user_dict, put_user_dict):
    response = client.put(
        f'/users/{response_user_dict["id"]}',
        json=put_user_dict    
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated['email'] == put_user_dict['email']
    assert updated['first_name'] == put_user_dict['first_name']
    assert updated['last_name'] == put_user_dict['last_name']


def test_put_non_exist_user(client, response_user_dict, put_user_dict):
    response = client.put(
        f'/users/{response_user_dict["id"]+1}',
        json=put_user_dict    
    )
    assert response.status_code == 404

