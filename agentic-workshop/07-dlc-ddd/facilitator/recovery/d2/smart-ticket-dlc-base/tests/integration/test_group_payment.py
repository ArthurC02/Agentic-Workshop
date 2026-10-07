from datetime import date
from smart_ticket.api.dependencies import gateway, reset_state
from smart_ticket.domain.models import BookingStatus, PaymentStatus


def test_group_success_creates_unique_order_and_rejects_repeat(client, create_group, memory_store):
    booking = create_group()
    prefix = f"/group-bookings/{booking['booking_id']}/pay"
    response = client.post(prefix)
    assert response.status_code == 200
    order = response.json()
    assert order["booking_id"] == booking["booking_id"]
    assert order["amount"] == booking["total_fare"] == 3500
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.PAID
    assert len(memory_store.orders) == 1
    assert memory_store.trips["T001"].available_seats == 15
    assert client.post(prefix).status_code == 409
    assert len(memory_store.orders) == 1


def test_group_failure_cancels_releases_every_seat_and_creates_no_order(client, create_group, memory_store):
    booking = create_group(count=20)
    gateway.next_result = PaymentStatus.FAILED
    response = client.post(f"/group-bookings/{booking['booking_id']}/pay")
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "PAYMENT_FAILED"
    stored = memory_store.bookings[booking["booking_id"]]
    assert stored.status == BookingStatus.CANCELLED
    assert not stored.seat_ids
    assert booking["booking_id"] not in memory_store.seat_assignments
    assert memory_store.trips["T001"].available_seats == 20
    assert not memory_store.orders


def test_generic_payment_route_cannot_bypass_group_compensation(client, create_group, memory_store):
    booking = create_group()
    gateway.next_result = PaymentStatus.FAILED
    assert client.post(f"/bookings/{booking['booking_id']}/pay").status_code == 409
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.CANCELLED
    assert memory_store.trips["T001"].available_seats == 20
    assert booking["booking_id"] not in memory_store.seat_assignments
    assert not memory_store.orders


def test_group_payment_endpoint_rejects_ordinary_booking(client, book_adult, memory_store, transaction_snapshot):
    booking = book_adult()
    before = transaction_snapshot()
    response = client.post(f"/group-bookings/{booking['booking_id']}/pay")
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "BOOKING_NOT_GROUP"
    assert transaction_snapshot() == before
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.PENDING_PAYMENT


def test_group_success_and_failure_record_audit_and_result_notifications(client, create_group):
    success = create_group()
    assert client.post(f"/group-bookings/{success['booking_id']}/pay").status_code == 200
    failed = create_group()
    gateway.next_result = PaymentStatus.FAILED
    assert client.post(f"/group-bookings/{failed['booking_id']}/pay").status_code == 409
    for booking, payment_event, notification_event in [
        (success, "GROUP_PAYMENT_COMPLETED", "GROUP_PAYMENT_COMPLETED"),
        (failed, "GROUP_PAYMENT_FAILED", "GROUP_BOOKING_CANCELLED")]:
        prefix = f"/bookings/{booking['booking_id']}"
        audit = client.get(prefix + "/audit-log")
        notify = client.get(prefix + "/notifications")
        assert audit.status_code == notify.status_code == 200
        assert {item["event"] for item in audit.json()} >= {"GROUP_BOOKING_CREATED", payment_event}
        assert notification_event in {item["event"] for item in notify.json()}


def test_cancelled_group_cannot_retry_or_double_release(client, create_group, memory_store):
    booking = create_group()
    url = f"/group-bookings/{booking['booking_id']}/pay"
    gateway.next_result = PaymentStatus.FAILED
    assert client.post(url).status_code == 409
    gateway.next_result = PaymentStatus.SUCCESS
    assert client.post(url).status_code == 409
    assert client.post(f"/bookings/{booking['booking_id']}/pay").status_code == 409
    assert memory_store.trips["T001"].available_seats == 20
    assert not memory_store.orders


def test_paid_group_refund_releases_all_seats_and_group_change_is_rejected(client, create_group, memory_store):
    booking = create_group()
    assert client.post(f"/group-bookings/{booking['booking_id']}/pay").status_code == 200
    prefix = f"/bookings/{booking['booking_id']}"
    assert client.post(prefix + "/change", json={"target_trip_id": "T006"}).status_code == 409
    assert memory_store.trips["T001"].available_seats == 15
    assert client.post(prefix + "/refund").status_code == 200
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.REFUNDED
    assert memory_store.trips["T001"].available_seats == 20
    assert booking["booking_id"] not in memory_store.seat_assignments


def test_reset_restores_group_ledgers_capacity_clock_and_gateway(create_group, memory_store, controlled_free_positions):
    create_group()
    memory_store.seat_capacity["T001"] = 42
    memory_store.clock.today = date(2029, 12, 31)
    gateway.next_result = PaymentStatus.FAILED
    reset_state()
    assert not memory_store.bookings and not memory_store.orders
    assert not memory_store.seat_assignments and not memory_store.audit_log and not memory_store.notifications
    assert not memory_store.refunds
    assert memory_store.seat_capacity["T001"] == memory_store.trips["T001"].available_seats == 20
    assert memory_store.clock.today == date(2030, 1, 14)
    assert gateway.next_result == PaymentStatus.SUCCESS
