import pytest
from control_api.api.dependencies import reset_dependencies_for_tests
from control_api.main import create_app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    reset_dependencies_for_tests()
    return TestClient(create_app())
