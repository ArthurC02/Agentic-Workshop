def test_optional_and_standard_member_preserve_adult_fare(client, book_adult):
    anonymous = book_adult()
    standard = book_adult(member_id="M001")
    assert anonymous["total_fare"] == standard["total_fare"] == 700
    response = client.get("/members/M001")
    assert response.status_code == 200
    assert response.json()["member_id"] == "M001"


def test_corporate_member_discount_and_invalid_member_atomic(client, book_adult, memory_store):
    corporate = book_adult(member_id="M002")
    assert corporate["total_fare"] == 665
    before = memory_store.trips["T001"].available_seats
    response = client.post("/bookings", json={"trip_id": "T001", "member_id": "missing",
        "passengers": [{"passenger_id": "A", "name": "Adult", "passenger_type": "ADULT"}]})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "MEMBER_NOT_FOUND"
    assert memory_store.trips["T001"].available_seats == before
    assert len(memory_store.bookings) == 1
