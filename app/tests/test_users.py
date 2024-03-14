import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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
