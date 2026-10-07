"""Acceptance tests for requirement card 03 (PCR-001 to PCR-014).

Seed trips depart 2030-01-15 09:00 (+08:00); the default Clock is 2030-01-14, so D = 1 (30% fee).
group_payload(mixed=True) makes odd indexes STUDENT: P0 adult, P1 student, P2 adult, ...
"""
import threading
import time
from datetime import date
import pytest
from smart_ticket.api import dependencies
from smart_ticket.domain import models
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.models import BookingStatus, PaymentStatus


@pytest.fixture
def paid_group(client, create_group):
    def create(**kwargs):
        booking = create_group(**kwargs)
        response = client.post(f"/group-bookings/{booking['booking_id']}/pay")
        assert response.status_code == 200, response.text
        return booking
    return create


@pytest.fixture
def cancel(client):
    def run(booking, passenger_ids, expected=200):
        response = client.post(f"/group-bookings/{booking['booking_id']}/cancel-passengers",
                               json={"passenger_ids": passenger_ids})
        assert response.status_code == expected, response.text
        return response.json()
    return run


@pytest.fixture
def ledger(client, memory_store):
    """PCR-008 read only through the API: (refunds, fees, active fares, Order.amount)."""
    def read(booking):
        booking_id = booking["booking_id"]
        current = client.get(f"/bookings/{booking_id}").json()
        refunds = client.get(f"/bookings/{booking_id}/refunds").json()
        active = [line["amount"] for line in current["applied_discounts"]
                  if line["passenger_id"] not in current["cancelled_passenger_ids"]]
        order = next(order for order in memory_store.orders.values() if order.booking_id == booking_id)
        return sum(r["amount"] for r in refunds), sum(r["fee"] for r in refunds), sum(active), order.amount
    return read


def error_code(response):
    return response["error"]["code"]


def test_pcr_001_only_group_bookings_without_points_can_cancel_passengers(client, book_adult, create_group,
                                                                           cancel, transaction_snapshot):
    individual = book_adult(pay=True, count=2)
    points = client.post("/group-bookings", json={"trip_id": "T001", "member_id": "M001", "redeemed_points": 1000,
                         "passengers": [{"passenger_id": f"P{i}", "name": "A", "passenger_type": "ADULT"}
                                        for i in range(6)]}).json()
    assert client.post(f"/group-bookings/{points['booking_id']}/pay").status_code == 200
    before = transaction_snapshot()
    assert error_code(cancel(individual, ["0"], 409)) == "PARTIAL_CANCEL_NOT_SUPPORTED"
    assert error_code(cancel(points, ["P0"], 409)) == "PARTIAL_CANCEL_NOT_SUPPORTED"
    assert transaction_snapshot() == before


def test_pcr_001_only_paid_group_bookings_can_cancel_passengers(client, create_group, paid_group, cancel,
                                                                transaction_snapshot):
    pending = create_group(count=6)
    refunded = paid_group(count=6)
    assert client.post(f"/bookings/{refunded['booking_id']}/refund").status_code == 200
    failed = create_group(count=6)
    dependencies.gateway.next_result = PaymentStatus.FAILED
    assert client.post(f"/group-bookings/{failed['booking_id']}/pay").status_code == 409
    before = transaction_snapshot()
    for booking in (pending, failed, refunded):
        assert error_code(cancel(booking, ["P0"], 409)) == "BOOKING_NOT_REFUNDABLE"
    assert transaction_snapshot() == before
    assert cancel({"booking_id": "missing"}, ["P0"], 404)["error"]["code"] == "BOOKING_NOT_FOUND"


def test_pcr_002_passengers_are_named_by_id_and_validated(client, paid_group, cancel, transaction_snapshot):
    booking = paid_group(count=7)
    other = paid_group(count=5)
    assert cancel(booking, ["P0", "P1"])["passenger_ids"] == ["P0", "P1"]
    before = transaction_snapshot()
    assert error_code(cancel(booking, ["X9"], 404)) == "PASSENGER_NOT_FOUND"
    assert error_code(cancel(other, ["P5"], 404)) == "PASSENGER_NOT_FOUND"      # P5 belongs to the 7-person group
    assert error_code(cancel(booking, ["P1"], 409)) == "PASSENGER_ALREADY_CANCELLED"
    cancel(booking, [], 422)
    cancel(booking, ["P2", "P2"], 422)
    assert client.post(f"/group-bookings/{booking['booking_id']}/cancel-passengers", json={}).status_code == 422
    assert transaction_snapshot() == before


@pytest.mark.parametrize("today", [date(2030, 1, 15), date(2030, 1, 16)])
def test_pcr_003_no_cancellation_on_or_after_the_departure_date(paid_group, cancel, clock, transaction_snapshot,
                                                                 today):
    booking = paid_group(count=6)
    clock.today = today
    before = transaction_snapshot()
    assert error_code(cancel(booking, ["P0"], 409)) == "REFUND_WINDOW_CLOSED"
    assert transaction_snapshot() == before


@pytest.mark.parametrize("today, days, fee, refund", [
    (date(2030, 1, 1), 14, 59, 536),    # card example: 10%, 59.5 floored
    (date(2030, 1, 2), 13, 119, 476),
    (date(2030, 1, 8), 7, 119, 476),    # card example: 20%
    (date(2030, 1, 9), 6, 178, 417),
    (date(2030, 1, 14), 1, 178, 417),   # 30%, 178.5 floored
])
def test_pcr_004_fee_band_follows_days_before_departure(paid_group, cancel, clock, today, days, fee, refund):
    clock.today = date(2030, 1, 1)            # bought 14 days ahead: every adult fare is ADVANCE 595
    booking = paid_group(count=6)
    assert {line["amount"] for line in booking["applied_discounts"]} == {595}
    clock.today = today
    assert (date(2030, 1, 15) - today).days == days
    record = cancel(booking, ["P0"])
    assert (record["fee"], record["amount"]) == (fee, refund)


def test_pcr_004_each_passenger_pays_a_fee_on_their_own_fare(paid_group, cancel):
    booking = paid_group(count=10, mixed=True)   # 5 adults 700 + 5 students 525; the 612.5 average is never used
    assert (cancel(booking, ["P0"])["fee"], cancel(booking, ["P1"])["fee"]) == (210, 157)
    record = cancel(booking, ["P3", "P5"])       # 157 + 157, not 1,050 x 30% = 315
    assert (record["fee"], record["amount"]) == (314, 736)
    assert all(isinstance(record[key], int) for key in ("fee", "amount"))


def test_pcr_005_group_keeps_at_least_five_active_passengers_or_none(paid_group, cancel, transaction_snapshot):
    booking = paid_group(count=6)
    cancel(booking, ["P0"])
    before = transaction_snapshot()
    assert error_code(cancel(booking, ["P1"], 409)) == "GROUP_BELOW_MINIMUM"
    assert error_code(cancel(booking, ["P1", "P2", "P3", "P4"], 409)) == "GROUP_BELOW_MINIMUM"
    assert transaction_snapshot() == before
    assert cancel(booking, ["P1", "P2", "P3", "P4", "P5"])["passenger_ids"] == ["P1", "P2", "P3", "P4", "P5"]


def test_pcr_005_concurrent_cancellations_cannot_break_the_minimum(paid_group, monkeypatch):
    booking = paid_group(count=6)
    # Widen the gap between "how many stay active?" and "mark cancelled" so an unlocked check-then-act interleaves.
    real_fee = models.cancellation_fee
    monkeypatch.setattr(models, "cancellation_fee", lambda fare, percent: time.sleep(0.05) or real_fee(fare, percent))
    start, outcomes = threading.Barrier(6), []

    def attempt(index):
        start.wait()
        try:
            dependencies.refund_service.cancel_passengers(booking["booking_id"], [f"P{index}"])
            outcomes.append("ok")
        except DomainError as error:
            outcomes.append(error.code)

    threads = [threading.Thread(target=attempt, args=(i,)) for i in range(6)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sorted(outcomes) == ["GROUP_BELOW_MINIMUM"] * 5 + ["ok"]
    assert len(dependencies.store.bookings[booking["booking_id"]].active_passenger_ids) == 5


def test_pcr_006_only_cancelled_seats_are_released_and_nobody_is_reseated(client, paid_group, cancel, book_adult,
                                                                          memory_store):
    booking = paid_group(count=6)
    seats = {seat["passenger_id"]: seat for seat in booking["assigned_seats"]}
    assert memory_store.trips["T001"].available_seats == 14
    cancel(booking, ["P2"])
    current = client.get(f"/bookings/{booking['booking_id']}").json()
    assert memory_store.trips["T001"].available_seats == 15
    assert current["assigned_seats"] == [seats[p] for p in ("P0", "P1", "P3", "P4", "P5")]   # S003 gap is fine
    assert current["seat_ids"] == ["S001", "S002", "S004", "S005", "S006"]
    assert [item.seat_id for item in memory_store.seat_assignments[booking["booking_id"]]] == current["seat_ids"]
    assert book_adult()["seat_ids"] == ["S003"]   # inventory really freed it


def test_pcr_007_every_partial_cancellation_adds_its_own_refund_record(client, paid_group, cancel, memory_store):
    booking = paid_group(count=7)
    first = cancel(booking, ["P0"])
    second = cancel(booking, ["P1"])
    assert first["refund_id"] != second["refund_id"]
    assert set(first) == {"refund_id", "booking_id", "passenger_ids", "fee", "amount", "created_at"}
    assert client.get(f"/bookings/{booking['booking_id']}/refunds").json() == [first, second]   # first not rewritten
    assert first["created_at"].startswith("2030-01-14T09:00:00")
    assert len(memory_store.refunds) == 2


def test_pcr_008_card_example_refunds_fees_and_active_fares_add_up_to_the_order(paid_group, cancel, ledger):
    booking = paid_group(count=6)
    assert ledger(booking) == (0, 0, 4200, 4200)
    assert (cancel(booking, ["P0"])["amount"], ledger(booking)) == (490, (490, 210, 3500, 4200))
    assert error_code(cancel(booking, ["P1"], 409)) == "GROUP_BELOW_MINIMUM"
    assert ledger(booking) == (490, 210, 3500, 4200)
    record = cancel(booking, ["P1", "P2", "P3", "P4", "P5"])
    assert (record["amount"], record["fee"]) == (2450, 1050)
    assert ledger(booking) == (2940, 1260, 0, 4200)


def test_pcr_008_holds_across_fee_bands_and_after_a_whole_refund(client, paid_group, cancel, clock, ledger):
    clock.today = date(2030, 1, 1)
    booking = paid_group(count=9, mixed=True)
    for today, ids in ((date(2030, 1, 1), ["P1"]), (date(2030, 1, 8), ["P0", "P3"]), (date(2030, 1, 14), ["P5"])):
        clock.today = today
        cancel(booking, ids)
        refunds, fees, active, paid = ledger(booking)
        assert refunds + fees + active == paid
    whole = paid_group(count=5)
    client.post(f"/bookings/{whole['booking_id']}/refund")
    assert ledger(whole) == (3500, 0, 0, 3500)


def test_pcr_009_booking_stays_paid_until_the_last_passenger_is_cancelled(client, paid_group, cancel):
    booking = paid_group(count=6)
    url = f"/bookings/{booking['booking_id']}"
    cancel(booking, ["P0"])
    assert client.get(url).json()["status"] == BookingStatus.PAID
    cancel(booking, ["P1", "P2", "P3", "P4", "P5"])
    assert client.get(url).json()["status"] == BookingStatus.REFUNDED
    assert client.get(url).json()["seat_ids"] == []


def test_pcr_010_booking_query_shows_cancelled_passengers_and_all_refunds(client, paid_group, cancel):
    booking, other = paid_group(count=7), paid_group(count=6)
    url = f"/bookings/{booking['booking_id']}"
    assert client.get(url).json()["cancelled_passenger_ids"] == []
    first, _, second = cancel(booking, ["P4"]), cancel(other, ["P0"]), cancel(booking, ["P6"])
    current = client.get(url).json()
    assert current["cancelled_passenger_ids"] == ["P4", "P6"]
    assert [p["passenger_id"] for p in current["passengers"]] == [f"P{i}" for i in range(7)]   # still listed
    assert client.get(url + "/refunds").json() == [first, second]
    assert client.get("/bookings/missing/refunds").status_code == 404


def test_pcr_011_a_failed_request_changes_nothing(paid_group, cancel, transaction_snapshot):
    booking = paid_group(count=7)
    cancel(booking, ["P0"])
    before = transaction_snapshot()
    assert error_code(cancel(booking, ["P1", "X9"], 404)) == "PASSENGER_NOT_FOUND"
    assert error_code(cancel(booking, ["P1", "P0"], 409)) == "PASSENGER_ALREADY_CANCELLED"
    assert error_code(cancel(booking, ["P1", "P2"], 409)) == "GROUP_BELOW_MINIMUM"
    assert transaction_snapshot() == before


def test_pcr_012_whole_refund_only_before_any_partial_cancellation(client, paid_group, cancel, memory_store):
    partly = paid_group(count=6)
    cancel(partly, ["P0"])
    response = client.post(f"/bookings/{partly['booking_id']}/refund")
    assert (response.status_code, error_code(response.json())) == (409, "BOOKING_NOT_REFUNDABLE")
    untouched = paid_group(count=5)
    record = client.post(f"/bookings/{untouched['booking_id']}/refund").json()
    assert (record["amount"], record["fee"]) == (3500, 0)
    assert record["passenger_ids"] == [f"P{i}" for i in range(5)]
    assert memory_store.trips["T001"].available_seats == 20 - 5


def test_pcr_013_cancellation_is_audited_and_notified(client, paid_group, cancel):
    booking = paid_group(count=7)
    cancel(booking, ["P0", "P1"])
    prefix = f"/bookings/{booking['booking_id']}"
    audit = [(e["event"], e["detail"]) for e in client.get(prefix + "/audit-log").json()]
    assert audit[-1] == ("PASSENGERS_CANCELLED", "passenger_ids=P0,P1 refund=980 fee=420")
    assert client.get(prefix + "/notifications").json()[-1]["event"] == "PASSENGERS_CANCELLED"


def test_pcr_014_cancellation_does_not_call_the_payment_gateway(paid_group, cancel, memory_store, monkeypatch):
    booking = paid_group(count=6)

    def no_gateway(*args):
        raise AssertionError("partial cancellation must not reach the payment gateway")

    monkeypatch.setattr(dependencies.gateway, "charge", no_gateway)
    cancel(booking, ["P0"])
    assert len(memory_store.orders) == 1
