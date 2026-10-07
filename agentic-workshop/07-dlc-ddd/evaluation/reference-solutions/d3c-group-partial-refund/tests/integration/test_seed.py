def test_full_seed_contains_eight_trips(client, memory_store):
    assert set(memory_store.trips) == {f"T{index:03d}" for index in range(1, 9)}
    response = client.get("/trips")
    assert response.status_code == 200
    assert {trip["trip_id"] for trip in response.json()} == {"T001", "T002", "T004", "T005", "T006", "T007", "T008"}
    assert memory_store.trips["T001"].base_fare == 700
    assert memory_store.trips["T005"].base_fare == 750


def test_member_seed_and_departure_times_are_fixed(client, memory_store):
    for member_id in ("M001", "M002", "M003"):
        assert client.get(f"/members/{member_id}").status_code == 200
    assert memory_store.trips["T001"].departure_time.isoformat() == "2030-01-15T09:00:00+08:00"
    assert all(trip.arrival_time > trip.departure_time for trip in memory_store.trips.values())


def test_member_seed_points_balances(client):
    balances = {member_id: client.get(f"/members/{member_id}").json()["points_balance"]
                for member_id in ("M001", "M002", "M003")}
    assert balances == {"M001": 1200, "M002": 5000, "M003": 0}
