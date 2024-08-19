from typing import Any, Generator

import pytest

from tests.utils.helper import set_test_dir_to_root


@pytest.fixture(autouse=True)
def setup_and_teardown() -> Generator[None, Any, None]:
    # Setup
    set_test_dir_to_root()

    # Test runner
    yield

    # Teardown
