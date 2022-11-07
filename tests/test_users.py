from app import schemas
import pytest
from jose import jwt
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("Hello"))
#     assert res.json().get("Hello") == "Everyone!"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "neca@gmail.com", "password": "123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "neca@gmail.com"
    assert res.status_code == 201


def test_login_server(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[
                         settings.algorithm])  # []
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wasdaasdl@gmail.com', '123', 403),
    ('neca@gmail.com', '34er2ge2d', 403),
    ('2134@gmail.com', 'frcxvbdsvd', 403),
    (None, '123', 422),
    ('neca@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})
    assert res.status_code == status_code
