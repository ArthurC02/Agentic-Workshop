import pytest
from fastapi.testclient import TestClient
from smart_ticket.api.dependencies import reset_state, store
from smart_ticket.main import app

@pytest.fixture(autouse=True)
def reset_store():
    reset_state()
    yield
    reset_state()

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def memory_store():
    return store
