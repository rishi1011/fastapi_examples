import pytest
from fastapi.testclient import TestClient

from proto_app.main import app

@pytest.fixture(scope="function")
def test_client():
    client = TestClient(app)
    yield client

