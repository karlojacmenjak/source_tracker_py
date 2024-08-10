from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from core.server import app

client: TestClient = TestClient(app=app)


@pytest.fixture(autouse=True)
def setup_and_teardown() -> Generator[None, Any, None]:
    # Setup

    # Test runner
    yield

    # Teardown


def test_can_connect_to_app():
    response = client.get("/")
    assert response.status_code == 200
