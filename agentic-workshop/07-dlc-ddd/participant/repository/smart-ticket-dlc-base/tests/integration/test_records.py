def test_booking_and_payment_append_queryable_audit_events(client, book_adult):
    booking = book_adult(pay=True)
    response = client.get(f"/bookings/{booking['booking_id']}/audit-log")
    assert response.status_code == 200
    records = response.json()
    assert len(records) >= 2
    assert {record["event"] for record in records} >= {"BOOKING_CREATED", "PAYMENT_COMPLETED"}
    assert all(record["booking_id"] == booking["booking_id"] for record in records)
    notifications = client.get(f"/bookings/{booking['booking_id']}/notifications")
    assert notifications.status_code == 200
    assert "PAYMENT_COMPLETED" in {record["event"] for record in notifications.json()}


def test_refund_creates_notification_and_audit_records(client, book_adult):
    booking = book_adult(pay=True)
    prefix = f"/bookings/{booking['booking_id']}"
    assert client.post(prefix + "/refund").status_code == 200
    notifications = client.get(prefix + "/notifications")
    audit = client.get(prefix + "/audit-log")
    assert notifications.status_code == audit.status_code == 200
    assert notifications.json()
    assert len(audit.json()) >= 3
    assert "BOOKING_REFUNDED" in {record["event"] for record in notifications.json()}
    assert "BOOKING_REFUNDED" in {record["event"] for record in audit.json()}
    assert all(record["booking_id"] == booking["booking_id"] for record in notifications.json())
