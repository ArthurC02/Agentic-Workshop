import pytest

def payload(count=1):
    return {"trip_id": "T001", "passengers": [
        {"passenger_id": f"P{i}", "name": f"測試旅客{i}", "passenger_type": "ADULT"}
        for i in range(count)]}

@pytest.mark.skip(reason="G0 TRIP-001, TRIP-002: implement trip query")
def test_sellable_trips(client):
    response = client.get("/trips?origin=台北")
    assert response.status_code == 200
    assert {trip["trip_id"] for trip in response.json()} == {"T001", "T002"}

@pytest.mark.skip(reason="G0 BOOKING-004, BOOKING-005: implement booking creation")
def test_booking_reserves_seat(client, memory_store):
    response = client.post("/bookings", json=payload())
    assert response.status_code == 201
    assert response.json()["status"] == "PENDING_PAYMENT"
    assert memory_store.trips["T001"].available_seats == 19

@pytest.mark.skip(reason="G0 BOOKING-002: implement passenger upper bound")
def test_more_than_four_rejected(client):
    assert 400 <= client.post("/bookings", json=payload(5)).status_code < 500

@pytest.mark.skip(reason="G0 BOOKING-003: implement remaining-seat check")
def test_insufficient_seats_rejected(client, memory_store):
    memory_store.trips["T001"].available_seats = 0
    assert 400 <= client.post("/bookings", json=payload()).status_code < 500

@pytest.mark.skip(reason="G0 PAYMENT-002, PAYMENT-003, ORDER-001: implement payment flow")
def test_payment_then_duplicate_rejected(client):
    booking_id = client.post("/bookings", json=payload()).json()["booking_id"]
    assert client.post(f"/bookings/{booking_id}/pay").status_code == 200
    assert 400 <= client.post(f"/bookings/{booking_id}/pay").status_code < 500

@pytest.mark.skip(reason="G0 ORDER-001, ORDER-002: implement order query")
def test_paid_order_query(client):
    booking_id = client.post("/bookings", json=payload()).json()["booking_id"]
    order = client.post(f"/bookings/{booking_id}/pay").json()
    response = client.get(f"/orders/{order['order_id']}")
    assert response.status_code == 200
    assert response.json()["amount"] == 700
