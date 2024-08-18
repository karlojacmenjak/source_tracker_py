from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import Response
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
    status_code_ok: bool = True
    content_is_html: bool = True


def test_can_connect_to_app() -> None:
    expected = CanConnectTestResults()

    response: Response = client.get("/")

    is_html = "text/html" in str(response.headers.get("content-type"))

    actual = CanConnectTestResults(
        status_code_ok=response.status_code == 200,
        content_is_html=is_html,
    )

    assert actual == expected
