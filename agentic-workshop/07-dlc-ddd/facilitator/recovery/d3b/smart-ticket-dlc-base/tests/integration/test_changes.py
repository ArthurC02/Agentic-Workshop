def test_paid_change_transfers_seats_and_records_fare_difference(client, book_adult, memory_store):
    booking = book_adult(pay=True)
    response = client.post(f"/bookings/{booking['booking_id']}/change", json={"target_trip_id": "T005"})
    assert response.status_code == 200, response.text
    assert response.json()["trip_id"] == "T005"
    assert response.json()["fare_difference"] == 50
    assert memory_store.trips["T001"].available_seats == 20
    assert memory_store.trips["T005"].available_seats == 5
    assert len(memory_store.orders) == 1
    assert next(iter(memory_store.orders.values())).amount == 700
    prefix = f"/bookings/{booking['booking_id']}"
    notifications = client.get(prefix + "/notifications")
    audit = client.get(prefix + "/audit-log")
    assert notifications.status_code == audit.status_code == 200
    assert "BOOKING_CHANGED" in {record["event"] for record in notifications.json()}
    assert "BOOKING_CHANGED" in {record["event"] for record in audit.json()}


def test_change_rejects_pending_missing_and_insufficient_target_atomically(client, book_adult, memory_store):
    pending = book_adult()
    url = f"/bookings/{pending['booking_id']}/change"
    assert client.post(url, json={"target_trip_id": "T005"}).status_code == 409
    paid = book_adult(pay=True)
    url = f"/bookings/{paid['booking_id']}/change"
    assert client.post(url, json={"target_trip_id": "missing"}).status_code == 404
    memory_store.trips["T005"].available_seats = 0
    assert client.post(url, json={"target_trip_id": "T005"}).status_code == 409
    assert memory_store.bookings[paid["booking_id"]].trip_id == "T001"
    assert memory_store.trips["T001"].available_seats == 18
    assert memory_store.trips["T005"].available_seats == 0
