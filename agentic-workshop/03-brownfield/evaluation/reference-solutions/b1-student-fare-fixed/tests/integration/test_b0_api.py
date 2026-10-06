def test_new_endpoints_report_missing_resources(client):
    assert client.get("/members/missing").status_code == 404
    for suffix in ("notifications", "audit-log"):
        response = client.get(f"/bookings/missing/{suffix}")
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "BOOKING_NOT_FOUND"
    assert client.post("/bookings/missing/change", json={"target_trip_id": "T005"}).status_code == 404
    assert client.post("/bookings/missing/refund").status_code == 404


def test_invalid_change_contract_does_not_mutate_booking(client, book_adult, memory_store):
    booking = book_adult(pay=True)
    response = client.post(f"/bookings/{booking['booking_id']}/change", json={})
    assert response.status_code == 422
    assert memory_store.bookings[booking["booking_id"]].trip_id == "T001"
    assert memory_store.trips["T001"].available_seats == 19
