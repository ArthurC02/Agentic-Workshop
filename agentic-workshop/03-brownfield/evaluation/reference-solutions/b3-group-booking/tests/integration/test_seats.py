from datetime import date
from smart_ticket.api.dependencies import reset_state, gateway
from smart_ticket.domain.models import PaymentStatus


def test_seat_ids_are_unique_and_capacity_failure_leaves_no_assignment(client, book_adult, memory_store):
    first = book_adult(count=2)
    second = book_adult(count=2)
    assignments = [item for group in memory_store.seat_assignments.values() for item in group]
    assert len(assignments) == 4
    assert len({item.seat_id for item in assignments}) == 4
    assert all(item.trip_id == "T001" for item in assignments)
    assert set(first["seat_ids"]).isdisjoint(second["seat_ids"])
    memory_store.trips["T001"].available_seats = 1
    response = client.post("/bookings", json={"trip_id": "T001", "passengers": [
        {"passenger_id": str(index), "name": "Adult", "passenger_type": "ADULT"} for index in range(2)]})
    assert response.status_code == 409
    assert len(memory_store.seat_assignments) == len(memory_store.bookings) == 2
    assert memory_store.trips["T001"].available_seats == 1


def test_reset_restores_seed_clock_gateway_and_all_transaction_ledgers(client, book_adult, memory_store):
    booking = book_adult(pay=True)
    assert client.post(f"/bookings/{booking['booking_id']}/refund").status_code == 200
    assert memory_store.refunds and memory_store.notifications and memory_store.audit_log
    memory_store.clock.today = date(2029, 12, 31)
    gateway.next_result = PaymentStatus.FAILED
    reset_state()
    assert memory_store.trips["T001"].available_seats == 20
    assert len(memory_store.trips) == 8
    assert not memory_store.bookings and not memory_store.orders
    assert not memory_store.seat_assignments and not memory_store.refunds
    assert not memory_store.notifications and not memory_store.audit_log
    assert memory_store.clock.today == date(2030, 1, 14)
    assert gateway.next_result == PaymentStatus.SUCCESS
