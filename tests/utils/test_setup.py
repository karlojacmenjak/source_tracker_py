from typing import Any, Callable, Generator

import pytest


@pytest.fixture(autouse=True)
def run_setup_and_teardown_tests(
    setup_func: Callable, teardown_func: Callable
) -> Generator[None, Any, None]:
    # Setup
    setup_func()

    # Test runner
    yield

    # Teardown
    teardown_func()
