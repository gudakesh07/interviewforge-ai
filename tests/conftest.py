import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_interviewforge.db"
os.environ["AI_PROVIDER"] = "mock"
os.environ["APP_SECRET_KEY"] = "test-secret"

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    if os.path.exists("test_interviewforge.db"):
        try:
            os.remove("test_interviewforge.db")
        except PermissionError:
            pass


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def registered_client(client: TestClient) -> TestClient:
    response = client.post(
        "/register",
        data={
            "username": "tester",
            "email": "tester@example.com",
            "password": "strong-password",
            "repeat_password": "strong-password",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    return client
