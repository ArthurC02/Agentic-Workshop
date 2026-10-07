from smart_ticket.domain.models import BookingStatus


def test_refund_releases_capacity_once_and_preserves_original_order(client, book_adult, memory_store):
    booking = book_adult(pay=True)
    url = f"/bookings/{booking['booking_id']}/refund"
    response = client.post(url)
    assert response.status_code == 200, response.text
    assert response.json()["booking_id"] == booking["booking_id"]
    assert response.json()["amount"] == 700
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.REFUNDED
    assert memory_store.trips["T001"].available_seats == 20
    assert len(memory_store.orders) == 1
    assert len(memory_store.refunds) == 1
    assert client.post(url).status_code == 409
    assert memory_store.trips["T001"].available_seats == 20
    assert len(memory_store.refunds) == 1


def test_pending_refund_is_rejected_without_releasing_reservation(client, book_adult, memory_store):
    booking = book_adult()
    assert client.post(f"/bookings/{booking['booking_id']}/refund").status_code == 409
    assert memory_store.bookings[booking["booking_id"]].status == BookingStatus.PENDING_PAYMENT
    assert memory_store.trips["T001"].available_seats == 19
    assert not memory_store.orders
