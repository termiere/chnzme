import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from app.services.auth import create_user, login
from app.schemas.auth import UserCreate, LoginRequest


def test_create_user():
    user = UserCreate(username="hello", password="bye")
    session = Mock()

    with patch(
        "app.services.auth.auth_repositories.find_user_by_username"
    ) as mock_find_user:
        mock_find_user.return_value = None

        with patch("app.services.auth.hash_password") as mock_hash_password:
            mock_hash_password.return_value = "hashed_password"

            with patch(
                "app.services.auth.auth_repositories.create_user"
            ) as mock_create_user:
                created_user = Mock(username="hello", id=1)
                mock_create_user.return_value = created_user
                result = create_user(session, user)
                assert result is created_user
                mock_find_user.assert_called_once_with(session, user.username)
                mock_hash_password.assert_called_once_with(user.password)
                mock_create_user.assert_called_once_with(
                    session, user.username, "hashed_password"
                )


def test_create_user_already_exists():
    user = UserCreate(username="hello", password="bye")
    session = Mock()
    existing_user = Mock(username="hello", id=1)

    with patch(
        "app.services.auth.auth_repositories.find_user_by_username"
    ) as mock_find_user:
        mock_find_user.return_value = existing_user

        with pytest.raises(HTTPException) as exc_info:
            with patch("app.services.auth.hash_password") as mock_hash_password:
                with patch(
                    "app.services.auth.auth_repositories.create_user"
                ) as mock_create_user:
                    create_user(session, user)

        assert exc_info.value.status_code == 409
        assert exc_info.value.detail == "пользователь уже существует"
        mock_hash_password.assert_not_called()
        mock_create_user.assert_not_called()


def test_login():
    credentials = LoginRequest(username="hello", password="bye")
    existing_user = Mock(username="hello", id=1, password_hash="hashed_password")
    session = Mock()

    with patch(
        "app.services.auth.auth_repositories.find_user_by_username"
    ) as mock_find_user:
        mock_find_user.return_value = existing_user

        with patch("app.services.auth.verify_password") as mock_verify_password:
            mock_verify_password.return_value = True

            with patch(
                "app.services.auth.create_access_token"
            ) as mock_create_access_token:
                mock_create_access_token.return_value = "test_access_token"

                result = login(session, credentials)
                assert result["access_token"] == "test_access_token"
                assert result["token_type"] == "bearer"

                mock_find_user.assert_called_once_with(session, credentials.username)
                mock_verify_password.assert_called_once_with(
                    credentials.password, existing_user.password_hash
                )
                mock_create_access_token.assert_called_once_with(existing_user.id)


def test_login_invalid_password():
    credentials = LoginRequest(username="hello", password="bye")
    existing_user = Mock(username="hello", id=1, password_hash="hashed_password")
    session = Mock()

    with patch(
        "app.services.auth.auth_repositories.find_user_by_username"
    ) as mock_find_user:
        mock_find_user.return_value = existing_user

        with pytest.raises(HTTPException) as exc_info:
            with patch("app.services.auth.verify_password") as mock_verify_password:
                mock_verify_password.return_value = False

                with patch(
                    "app.services.auth.create_access_token"
                ) as mock_create_access_token:
                    login(session, credentials)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "неверный username или пароль"
        mock_verify_password.assert_called_once_with(
            credentials.password,
            existing_user.password_hash,
        )
        mock_create_access_token.assert_not_called()


def test_login_user_not_found():
    credentials = LoginRequest(username="hello", password="bye")
    session = Mock()

    with pytest.raises(HTTPException) as exc_info:
        with patch(
            "app.services.auth.auth_repositories.find_user_by_username"
        ) as mock_find_user_by_username:
            mock_find_user_by_username.return_value = None

            with patch("app.services.auth.verify_password") as mock_verify_password:
                with patch(
                    "app.services.auth.create_access_token"
                ) as mock_create_access_token:
                    login(session, credentials)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "неверный username или пароль"

    mock_find_user_by_username.assert_called_once_with(session, credentials.username)
    mock_verify_password.assert_not_called()
    mock_create_access_token.assert_not_called()
