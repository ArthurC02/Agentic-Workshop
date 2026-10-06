from copy import deepcopy
from datetime import date


def mixed_payload(member_id=None):
    body = {"trip_id": "T001", "passengers": [
        {"passenger_id": "A", "name": "Adult", "passenger_type": "ADULT"},
        {"passenger_id": "S", "name": "Student", "passenger_type": "STUDENT"}]}
    if member_id:
        body["member_id"] = member_id
    return body


def test_mixed_triple_eligibility_exposes_per_passenger_discount_without_stacking(client, memory_store):
    memory_store.clock.today = date(2030, 1, 1)
    body = mixed_payload("M002")
    response = client.post("/bookings", json=body)
    assert response.status_code == 201
    booking = response.json()
    assert booking["passengers"] == body["passengers"]
    assert booking["applied_discounts"] == [
        {"passenger_id": "A", "discount_type": "ADVANCE", "rate": 85, "amount": 595},
        {"passenger_id": "S", "discount_type": "STUDENT", "rate": 75, "amount": 525}]
    assert booking["total_fare"] == 1120
    assert memory_store.trips["T001"].available_seats == 18


def test_corporate_student_selects_student_rate_even_without_advance(client):
    body = mixed_payload("M002")
    body["passengers"] = body["passengers"][1:]
    response = client.post("/bookings", json=body)
    assert response.status_code == 201
    assert response.json()["total_fare"] == 525
    assert response.json()["applied_discounts"] == [
        {"passenger_id": "S", "discount_type": "STUDENT", "rate": 75, "amount": 525}]


def test_change_reprices_each_passenger_with_same_policy_and_preserves_paid_order(client, memory_store):
    created = client.post("/bookings", json=mixed_payload())
    assert created.status_code == 201
    booking = created.json()
    assert booking["total_fare"] == 1225
    paid = client.post(f"/bookings/{booking['booking_id']}/pay")
    assert paid.status_code == 200
    memory_store.clock.today = date(2030, 1, 1)
    response = client.post(f"/bookings/{booking['booking_id']}/change", json={"target_trip_id": "T005"})
    assert response.status_code == 200
    changed = response.json()
    assert changed["applied_discounts"] == [
        {"passenger_id": "A", "discount_type": "ADVANCE", "rate": 85, "amount": 637},
        {"passenger_id": "S", "discount_type": "STUDENT", "rate": 75, "amount": 562}]
    assert changed["total_fare"] == 1199
    assert changed["fare_difference"] == -26
    assert memory_store.orders[paid.json()["order_id"]].amount == 1225
    assert memory_store.trips["T001"].available_seats == 20
    assert memory_store.trips["T005"].available_seats == 4


def test_failed_change_preserves_fare_discount_and_all_ledgers_atomically(client, memory_store):
    response = client.post("/bookings", json=mixed_payload("M002"))
    assert response.status_code == 201
    booking_id = response.json()["booking_id"]
    assert client.post(f"/bookings/{booking_id}/pay").status_code == 200
    memory_store.trips["T005"].available_seats = 1
    before = deepcopy((memory_store.bookings, memory_store.orders, memory_store.seat_assignments,
                       memory_store.audit_log, memory_store.notifications))
    memory_store.clock.today = date(2030, 1, 1)
    failed = client.post(f"/bookings/{booking_id}/change", json={"target_trip_id": "T005"})
    assert failed.status_code == 409
    assert failed.json()["error"]["code"] == "INSUFFICIENT_SEATS"
    assert (memory_store.bookings, memory_store.orders, memory_store.seat_assignments,
            memory_store.audit_log, memory_store.notifications) == before
    assert memory_store.trips["T001"].available_seats == 18
    assert memory_store.trips["T005"].available_seats == 1
