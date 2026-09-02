import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.dependency import get_session
from app.database import Base

from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def test_database_url(self):
        return f"postgresql+psycopg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env.test")


test_settings = TestSettings()

test_engine = create_engine(url=test_settings.test_database_url)

test_session_factory = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
)


def get_test_session():
    with test_session_factory() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture(autouse=True)
def setup_session():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session():
    with test_session_factory() as session:
        yield session


@pytest.fixture()
def registered_user(client):
    user_data = {
        "username": "hello",
        "password": "bye",
    }
    response = client.post(
        url="/api/v1/auth/register",
        json=user_data,
    )
    assert response.status_code == 200
    return user_data


@pytest.fixture()
def auth_token(client, registered_user):
    payload = {
        "username": registered_user["username"],
        "password": registered_user["password"],
    }
    response = client.post(url="/api/v1/auth/login", json=payload)
    response_data = response.json()

    assert response.status_code == 200
    assert "access_token" in response_data
    assert response_data["access_token"] is not None

    token = response_data["access_token"]
    return token
