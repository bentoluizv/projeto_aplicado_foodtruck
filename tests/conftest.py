import pytest
from fastapi.testclient import TestClient

from projeto_aplicado.app import app


@pytest.fixture
def client():
    return TestClient(app)
