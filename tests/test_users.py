import pytest
from app import schemas
from app.config import settings
from jose import jwt


def test_create_user(client):
    res = client.post("/users/", json={
        "first_name": "Rafaay",
        "last_name": "Shaheen",
        "email": "Rafaay@gmail.com",
        "password": "123456789"
    })
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.first_name == "Rafaay"
    assert new_user.last_name == "Shaheen"
    assert new_user.email == "Rafaay@gmail.com"

    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username": test_user['email'],
        "password": test_user['password']
    })

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm)
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrognEmail@gmail.com', '123456789', 403),
    ('haider@gmail.com', 'wrongPassword', 403),
    ('wrongEmail@gmail.com', 'wrongPassword', 403),
    (None, '123456789', 422),
    ('haider@gmail.com', None, 422),
    (None, None, 422),
])
def test_login_unsuccessful(client, test_user, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password
    })

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"
    