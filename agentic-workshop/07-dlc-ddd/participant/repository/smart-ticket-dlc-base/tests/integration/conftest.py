from copy import deepcopy
import pytest
from smart_ticket.domain.records import SeatAssignment


@pytest.fixture
def group_payload():
    def build(count=5, trip_id="T001", member_id=None, mixed=False):
        result = {"trip_id": trip_id, "passengers": [
            {"passenger_id": f"P{index}", "name": f"Passenger {index}",
             "passenger_type": "STUDENT" if mixed and index % 2 else "ADULT"}
            for index in range(count)]}
        if member_id:
            result["member_id"] = member_id
        return result
    return build


@pytest.fixture
def create_group(client, group_payload):
    def create(**kwargs):
        response = client.post("/group-bookings", json=group_payload(**kwargs))
        assert response.status_code == 201, response.text
        return response.json()
    return create


@pytest.fixture
def transaction_snapshot(memory_store):
    def snapshot():
        return deepcopy((memory_store.bookings, memory_store.orders, memory_store.seat_assignments,
            memory_store.refunds, memory_store.audit_log, memory_store.notifications,
            {key: trip.available_seats for key, trip in memory_store.trips.items()}))
    return snapshot


@pytest.fixture
def controlled_free_positions(memory_store):
    def configure(free, capacity=20):
        memory_store.seat_capacity["T001"] = capacity
        memory_store.trips["T001"].available_seats = len(free)
        memory_store.seat_assignments["occupied"] = [
            SeatAssignment("occupied", f"O{position}", "T001", f"S{position:03d}")
            for position in range(1, capacity + 1) if position not in free]
    return configure
