from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from utils import set_test_dir_to_root

from core.server import app

client: TestClient = TestClient(app=app)


@pytest.fixture(autouse=True)
def setup_and_teardown() -> Generator[None, Any, None]:
    # Setup
    set_test_dir_to_root()

    # Test runner
    yield

    # Teardown


class CanConnectTestResults(BaseModel):
    status_code_ok: bool


def test_can_connect_to_app() -> None:
    expected = CanConnectTestResults(status_code_ok=True)

    response = client.get("/")

    actual = CanConnectTestResults(status_code_ok=response.status_code == 200)

    assert actual == expected
