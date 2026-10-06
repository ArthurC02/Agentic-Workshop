import pytest
from datetime import date
from pathlib import Path
from fastapi.testclient import TestClient
from smart_ticket.api.dependencies import reset_state, store
from smart_ticket.main import app

@pytest.fixture(autouse=True)
def reset_store(request):
    reset_state()
    # Preserve original G1 assertions under their original data context.
    regression_files = {"test_health.py", "test_fare_policy.py", "test_services.py", "test_features.py"}
    if Path(str(request.node.fspath)).name in regression_files:
        store.trips = {key: trip for key, trip in store.trips.items() if key in {"T001", "T002", "T003", "T004"}}
    store.clock.today = date(2030, 1, 14)
    yield
    reset_state()

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def memory_store():
    return store


@pytest.fixture
def book_adult(client):
    def create(trip_id="T001", member_id=None, pay=False, count=1):
        body = {"trip_id": trip_id, "passengers": [
            {"passenger_id": str(index), "name": "Adult", "passenger_type": "ADULT"}
            for index in range(count)]}
        if member_id is not None:
            body["member_id"] = member_id
        response = client.post("/bookings", json=body)
        assert response.status_code == 201, response.text
        booking = response.json()
        if pay:
            result = client.post(f"/bookings/{booking['booking_id']}/pay")
            assert result.status_code == 200, result.text
        return booking
    return create
