"""Acceptance tests for requirement card 02 (PTS-001 to PTS-015).

Clock is the default 2030-01-14, so no passenger gets the advance discount.
Seed balances: M001 1,200 points, M002 5,000, M003 0.
"""
import threading
import time
import pytest
from smart_ticket.api import dependencies
from smart_ticket.domain import members
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.models import BookingStatus, Passenger, PassengerType, PaymentStatus

ADULT = {"passenger_id": "A", "name": "Adult", "passenger_type": "ADULT"}
STUDENT = {"passenger_id": "S", "name": "Student", "passenger_type": "STUDENT"}


def adults(count):
    return [{"passenger_id": f"G{i}", "name": f"G{i}", "passenger_type": "ADULT"} for i in range(count)]


@pytest.fixture
def book(client):
    def create(passengers=(ADULT,), member_id="M001", points=None, trip_id="T001", expected=201):
        body = {"trip_id": trip_id, "passengers": list(passengers), "member_id": member_id}
        if points is not None:
            body["redeemed_points"] = points
        url = "/group-bookings" if len(passengers) >= 5 else "/bookings"
        response = client.post(url, json=body)
        assert response.status_code == expected, response.text
        return response.json()
    return create


@pytest.fixture
def pay(client):
    def run(booking, expected=200):
        prefix = "/group-bookings" if booking["booking_type"] == "GROUP" else "/bookings"
        response = client.post(f"{prefix}/{booking['booking_id']}/pay")
        assert response.status_code == expected, response.text
        return response.json()
    return run


@pytest.fixture
def balance(client):
    return lambda member_id="M001": client.get(f"/members/{member_id}").json()["points_balance"]


@pytest.fixture
def audit(client):
    def entries(booking_id):
        return [(e["event"], e["detail"]) for e in client.get(f"/bookings/{booking_id}/audit-log").json()
                if e["event"].startswith("POINTS_")]
    return entries


# The card's worked examples: (passengers, member, points, discounted total, payable)
WORKED_EXAMPLES = [
    ((ADULT,), "M001", 200, 700, 500),
    ((ADULT,), "M002", 100, 665, 565),               # corporate 95%; cap 199
    (tuple(adults(5)), "M001", 1000, 3500, 2500),    # group; cap 1,050
    ((ADULT, STUDENT), "M001", 300, 1225, 925),      # cap 367
]


@pytest.mark.parametrize("points", [None, 0])
@pytest.mark.parametrize("passengers", [(ADULT,), tuple(adults(5))], ids=["individual", "group"])
def test_pts_001_points_are_optional_and_zero_changes_nothing(book, pay, balance, audit, passengers, points):
    booking = book(passengers, points=points)
    assert booking["redeemed_points"] == 0
    assert booking["payable_amount"] == booking["total_fare"]
    assert pay(booking)["amount"] == booking["total_fare"]
    assert balance() == 1200
    assert audit(booking["booking_id"]) == []


@pytest.mark.parametrize("passengers", [(ADULT,), tuple(adults(5))], ids=["individual", "group"])
def test_pts_002_points_require_a_member(book, memory_store, passengers):
    error = book(passengers, member_id=None, points=100, expected=409)
    assert error["error"]["code"] == "POINTS_MEMBER_REQUIRED"
    assert not memory_store.bookings


@pytest.mark.parametrize("points", [-100, 50, 99, 150, 250])
def test_pts_003_points_below_100_or_not_a_multiple_of_100_are_rejected(book, balance, points):
    assert book(points=points, expected=409)["error"]["code"] == "POINTS_INVALID_AMOUNT"
    assert balance() == 1200


def test_pts_004_points_above_the_balance_are_rejected(book, balance):
    assert book(member_id="M003", points=100, expected=409)["error"]["code"] == "POINTS_INSUFFICIENT"
    # 1,300 is above both the balance (1,200) and the cap (1,050): the balance is checked first.
    assert book(adults(5), points=1300, expected=409)["error"]["code"] == "POINTS_INSUFFICIENT"
    assert balance("M003") == 0 and balance() == 1200


@pytest.mark.parametrize("passengers, member_id, points", [
    ((ADULT,), "M001", 300),            # 700 -> cap 210
    ((ADULT,), "M002", 200),            # 665 -> cap 199.5 floored to 199 (the base fare would allow 210)
    ((ADULT, STUDENT), "M001", 400),    # 1,225 -> cap 367
])
def test_pts_005_points_above_30_percent_of_the_discounted_total_are_rejected(book, balance, passengers, member_id, points):
    assert book(passengers, member_id, points, expected=409)["error"]["code"] == "POINTS_EXCEED_LIMIT"
    assert balance(member_id) in (1200, 5000)


def test_pts_005_cap_itself_is_allowed(book):
    booking = book(adults(2), points=900, trip_id="T002")   # 3,000 -> cap exactly 900
    assert booking["payable_amount"] == 2100


@pytest.mark.parametrize("passengers, member_id", [((ADULT,), "M002"), ((ADULT, STUDENT), "M001")])
def test_pts_006_points_do_not_change_discounts(book, passengers, member_id):
    without = book(passengers, member_id)
    redeemed = book(passengers, member_id, points=100)
    assert redeemed["applied_discounts"] == without["applied_discounts"]
    assert redeemed["total_fare"] == without["total_fare"]
    assert redeemed["payable_amount"] == without["total_fare"] - 100


@pytest.mark.parametrize("passengers, member_id, points, total, payable", WORKED_EXAMPLES)
def test_pts_007_booking_shows_total_redeemed_points_and_payable(client, book, balance, passengers,
                                                                 member_id, points, total, payable):
    created = book(passengers, member_id, points)
    queried = client.get(f"/bookings/{created['booking_id']}").json()
    for booking in (created, queried):
        assert (booking["total_fare"], booking["redeemed_points"], booking["payable_amount"]) == (total, points, payable)
    assert balance(member_id) == {"M001": 1200, "M002": 5000}[member_id] - points   # PTS-008: reserved at once


@pytest.mark.parametrize("member_id, points", [(None, 100), ("M001", 50), ("M003", 100), ("M001", 300)],
                         ids=["no-member", "invalid", "insufficient", "over-limit"])
def test_pts_008_failed_redemption_creates_no_booking_seats_or_deduction(book, balance, memory_store, member_id, points):
    book(member_id=member_id, points=points, expected=409)
    assert not memory_store.bookings and not memory_store.seat_assignments and not memory_store.audit_log
    assert memory_store.trips["T001"].available_seats == 20
    assert (balance("M001"), balance("M003")) == (1200, 0)


def test_pts_008_group_without_consecutive_seats_keeps_points(book, balance, controlled_free_positions, memory_store):
    controlled_free_positions(free={1, 2, 3, 5, 6, 7, 9, 10})
    assert book(adults(5), points=1000, expected=409)["error"]["code"] == "CONSECUTIVE_SEATS_UNAVAILABLE"
    assert balance() == 1200 and not memory_store.bookings


@pytest.mark.parametrize("passengers, points, charged, sales, tax", [
    ((ADULT,), 200, 500, 476, 24),
    (tuple(adults(5)), 1000, 2500, 2381, 119),
], ids=["individual", "group"])
def test_pts_009_gateway_charges_payable_and_order_and_invoice_use_it(book, pay, monkeypatch,
                                                                      passengers, points, charged, sales, tax):
    calls = []
    real_charge = dependencies.gateway.charge
    monkeypatch.setattr(dependencies.gateway, "charge",
                        lambda booking_id, amount: calls.append(amount) or real_charge(booking_id, amount))
    order = pay(book(passengers, points=points))
    assert calls == [charged] and order["amount"] == charged
    invoice = dependencies.invoice_provider.received[0]   # D3a: invoice total is Order.amount
    assert (invoice["total_amount"], invoice["sales_amount"], invoice["tax_amount"]) == (charged, sales, tax)


def test_pts_010_group_payment_failure_restores_all_points(book, pay, balance, audit, memory_store):
    booking = book(adults(5), points=1000)
    dependencies.gateway.next_result = PaymentStatus.FAILED
    pay(booking, expected=409)
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.CANCELLED
    assert balance() == 1200
    assert ("POINTS_RESTORED", "points=1000") in audit(booking["booking_id"])


def test_pts_011_individual_payment_failure_keeps_points_reserved(book, pay, balance, audit, memory_store):
    booking = book(points=200)
    dependencies.gateway.next_result = PaymentStatus.FAILED
    pay(booking, expected=409)
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.PENDING_PAYMENT
    assert balance() == 1000
    assert [event for event, _ in audit(booking["booking_id"])] == ["POINTS_RESERVED"]
    dependencies.gateway.next_result = PaymentStatus.SUCCESS
    assert pay(booking)["amount"] == 500   # paying again later still charges the payable amount


@pytest.mark.parametrize("passengers, points, paid", [((ADULT,), 200, 500), (tuple(adults(5)), 1000, 2500)],
                         ids=["individual", "group"])
def test_pts_012_refund_returns_paid_cash_and_all_points(client, book, pay, balance, audit, passengers, points, paid):
    booking = book(passengers, points=points)
    pay(booking)
    refund = client.post(f"/bookings/{booking['booking_id']}/refund").json()
    assert refund["amount"] == paid
    assert balance() == 1200
    assert ("POINTS_RESTORED", f"points={points}") in audit(booking["booking_id"])


def test_pts_012_refund_after_change_returns_order_amount_not_the_new_fare(client, book, pay, balance):
    booking = book(points=200)
    pay(booking)
    client.post(f"/bookings/{booking['booking_id']}/change", json={"target_trip_id": "T005"})   # 750
    assert client.post(f"/bookings/{booking['booking_id']}/refund").json()["amount"] == 500
    assert balance() == 1200


def test_pts_013_change_keeps_redeemed_points_and_fare_difference_uses_totals(client, book, pay, balance, audit, memory_store):
    booking = book(points=200)
    order = pay(booking)
    changed = client.post(f"/bookings/{booking['booking_id']}/change", json={"target_trip_id": "T005"}).json()
    assert (changed["total_fare"], changed["redeemed_points"], changed["fare_difference"]) == (750, 200, 50)
    assert memory_store.orders[order["order_id"]].amount == 500
    assert balance() == 1000
    assert [event for event, _ in audit(booking["booking_id"])] == ["POINTS_RESERVED"]


def test_pts_014_reservations_never_exceed_the_balance(book, balance):
    book(points=200)
    book(adults(5), points=1000)
    assert book(points=100, expected=409)["error"]["code"] == "POINTS_INSUFFICIENT"
    assert balance() == 0


def test_pts_014_concurrent_bookings_cannot_overdraw(monkeypatch, balance):
    # Widen the gap between "enough points?" and "deduct" so an unlocked check-then-act would interleave.
    real_cap = members.redemption_cap
    monkeypatch.setattr(members, "redemption_cap", lambda total: time.sleep(0.05) or real_cap(total))
    start, outcomes = threading.Barrier(8), []

    def attempt(index):
        start.wait()
        try:
            dependencies.booking_service.create(
                "T001", [Passenger(f"P{index}", "Adult", PassengerType.ADULT)], "M001", 200)
            outcomes.append("ok")
        except DomainError as error:
            outcomes.append(error.code)

    threads = [threading.Thread(target=attempt, args=(i,)) for i in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sorted(outcomes) == ["POINTS_INSUFFICIENT"] * 2 + ["ok"] * 6
    assert balance() == 0


def test_pts_015_reservation_and_restoration_are_audited_with_the_points(book, pay, audit):
    booking = book(adults(5), points=700)
    dependencies.gateway.next_result = PaymentStatus.FAILED
    pay(booking, expected=409)
    assert audit(booking["booking_id"]) == [("POINTS_RESERVED", "points=700"), ("POINTS_RESTORED", "points=700")]
