from datetime import date
import pytest


@pytest.mark.parametrize("count,status", [(4, 409), (5, 201), (20, 201), (21, 409)],
                         ids=["four-rejected", "five-accepted", "twenty-accepted", "twenty-one-rejected"])
def test_group_size_boundaries(count, status, client, group_payload, memory_store, transaction_snapshot):
    before = transaction_snapshot()
    response = client.post("/group-bookings", json=group_payload(count=count))
    assert response.status_code == status, response.text
    if status == 409:
        assert response.json()["error"]["code"] == "INVALID_GROUP_SIZE"
        assert transaction_snapshot() == before
    else:
        booking = response.json()
        assert booking["booking_type"] == "GROUP"
        assert booking["status"] == "PENDING_PAYMENT"
        assert memory_store.trips["T001"].available_seats == 20 - count
        seats = booking["assigned_seats"]
        assert len(seats) == count
        assert len({seat["carriage_id"] for seat in seats}) == 1
        assert {seat["trip_id"] for seat in seats} == {"T001"}
        assert [seat["position"] for seat in seats] == list(range(1, count + 1))


def test_group_insufficient_total_capacity_is_atomic(client, group_payload, transaction_snapshot):
    before = transaction_snapshot()
    response = client.post("/group-bookings", json=group_payload(count=20, trip_id="T006"))
    assert response.status_code == 409
    assert transaction_snapshot() == before


def test_group_missing_trip_is_atomic(client, group_payload, transaction_snapshot):
    before = transaction_snapshot()
    response = client.post("/group-bookings", json=group_payload(trip_id="missing"))
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TRIP_NOT_FOUND"
    assert transaction_snapshot() == before


def test_group_invalid_member_is_atomic(client, group_payload, transaction_snapshot):
    before = transaction_snapshot()
    response = client.post("/group-bookings", json=group_payload(member_id="missing"))
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "MEMBER_NOT_FOUND"
    assert transaction_snapshot() == before


def test_fragmented_free_seats_do_not_create_partial_group(client, group_payload, controlled_free_positions, transaction_snapshot):
    controlled_free_positions({1, 3, 5, 7, 9, 11})
    before = transaction_snapshot()
    response = client.post("/group-bookings", json=group_payload())
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "CONSECUTIVE_SEATS_UNAVAILABLE"
    assert transaction_snapshot() == before


def test_contiguous_global_ids_cannot_cross_carriage(client, group_payload, controlled_free_positions, transaction_snapshot):
    controlled_free_positions({19, 20, 21, 22, 23}, capacity=42)
    before = transaction_snapshot()
    response = client.post("/group-bookings", json=group_payload())
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "CONSECUTIVE_SEATS_UNAVAILABLE"
    assert transaction_snapshot() == before


def test_contiguous_seats_can_cross_rows_inside_one_carriage(create_group, controlled_free_positions):
    controlled_free_positions({3, 4, 5, 6, 7})
    booking = create_group()
    seats = booking["assigned_seats"]
    assert [seat["position"] for seat in seats] == [3, 4, 5, 6, 7]
    assert len({seat["row_number"] for seat in seats}) == 2
    assert {seat["carriage_id"] for seat in seats} == {"C001"}


def test_group_mixed_fares_apply_b2_policy_per_passenger(create_group, memory_store):
    memory_store.clock.today = date(2030, 1, 1)
    booking = create_group(member_id="M002", mixed=True)
    details = booking["applied_discounts"]
    assert len(details) == 5
    assert [(item["discount_type"], item["rate"], item["amount"]) for item in details] == [
        ("ADVANCE", 85, 595), ("STUDENT", 75, 525), ("ADVANCE", 85, 595),
        ("STUDENT", 75, 525), ("ADVANCE", 85, 595)]
    assert [item["passenger_id"] for item in details] == [f"P{index}" for index in range(5)]
    assert booking["total_fare"] == sum(item["amount"] for item in details) == 2835


def test_group_searches_second_carriage_when_first_is_full(create_group, controlled_free_positions):
    controlled_free_positions({21, 22, 23, 24, 25}, capacity=42)
    booking = create_group()
    assert {seat["carriage_id"] for seat in booking["assigned_seats"]} == {"C002"}
    assert [seat["position"] for seat in booking["assigned_seats"]] == [1, 2, 3, 4, 5]
    assert [seat["seat_id"] for seat in booking["assigned_seats"]] == [f"S{index:03d}" for index in range(21, 26)]
