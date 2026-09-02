def test_register(client):
    payload = {
        "username": "hello",
        "password": "bye",
    }
    response = client.post(url="/api/v1/auth/register", json=payload)
    response_data = response.json()

    assert response.status_code == 200
    assert isinstance(response_data["id"], int)
    assert response_data["username"] == payload["username"]


def test_re_register(client, registered_user):
    payload = {
        "username": registered_user["username"],
        "password": registered_user["password"],
    }

    response = client.post(url="/api/v1/auth/register", json=payload)
    response_data = response.json()

    assert response.status_code == 409
    assert response_data["detail"] == "пользователь уже существует"


def test_login_success(client, registered_user):
    payload = {
        "username": registered_user["username"],
        "password": registered_user["password"],
    }

    response = client.post(url="/api/v1/auth/login", json=payload)
    response_data = response.json()

    assert response.status_code == 200
    assert "access_token" in response_data
    assert isinstance(response_data["access_token"], str)


def test_login_invalid_password(client, registered_user):
    payload = {
        "username": registered_user["username"],
        "password": "false",
    }

    response = client.post(url="/api/v1/auth/login", json=payload)
    response_data = response.json()

    assert response.status_code == 401
    assert response_data["detail"] == "неверный username или пароль"


def test_login_nonexistent_user(client):
    response = client.post(
        url="/api/v1/auth/login",
        json={
            "username": "hello",
            "password": "false",
        },
    )

    response_data = response.json()

    assert response.status_code == 401
    assert response_data["detail"] == "неверный username или пароль"


def test_me_with_valid_token(client, registered_user, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(
        url="/api/v1/auth/me",
        headers=headers,
    )

    response_data = response.json()
    assert response.status_code == 200
    assert isinstance(response_data["id"], int)
    assert response_data["username"] == registered_user["username"]


def test_me_without_token(client):
    response = client.get(
        url="/api/v1/auth/me",
    )
    response_data = response.json()

    assert response.status_code == 401
    assert response_data["detail"] == "Not authenticated"


def test_me_with_invalid_token(client):
    incorrect_jwt = "falsejwt"
    headers = {"Authorization": f"Bearer {incorrect_jwt}"}
    response = client.get(
        url="/api/v1/auth/me",
        headers=headers,
    )
    response_data = response.json()
    assert response.status_code == 401
    assert response_data["detail"] == "неверный токен"
