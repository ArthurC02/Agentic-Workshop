import pytest

from smart_ticket.application.booking_service import BookingService
from smart_ticket.application.order_service import OrderService
from smart_ticket.application.payment_service import PaymentService
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.models import BookingStatus, Passenger, PassengerType, PaymentStatus
from smart_ticket.infrastructure.payment_gateway import MockPaymentGateway


def passengers(count):
    return [Passenger(str(index), f"Passenger {index}", PassengerType.ADULT) for index in range(count)]


def booking_service(store):
    return BookingService(store, FarePolicy())


def assert_domain_error(exc, code, status):
    assert exc.value.code == code
    assert exc.value.status_code == status


def test_zero_passengers_rejected_without_mutating_store(memory_store):
    before = memory_store.trips["T001"].available_seats
    with pytest.raises(DomainError) as exc:
        booking_service(memory_store).create("T001", [])
    assert_domain_error(exc, "INVALID_PASSENGER_COUNT", 409)
    assert memory_store.trips["T001"].available_seats == before
    assert memory_store.bookings == {}
    assert memory_store.orders == {}


def test_five_passengers_rejected_without_mutating_store(memory_store):
    before = memory_store.trips["T001"].available_seats
    with pytest.raises(DomainError) as exc:
        booking_service(memory_store).create("T001", passengers(5))
    assert_domain_error(exc, "INVALID_PASSENGER_COUNT", 409)
    assert memory_store.trips["T001"].available_seats == before
    assert memory_store.bookings == {}
    assert memory_store.orders == {}


def test_four_passengers_are_accepted(memory_store):
    booking = booking_service(memory_store).create("T001", passengers(4))
    assert len(booking.passengers) == 4
    assert booking.total_fare == 2800
    assert memory_store.trips["T001"].available_seats == 16


def test_insufficient_seats_rejected_atomically(memory_store):
    memory_store.trips["T001"].available_seats = 1
    with pytest.raises(DomainError) as exc:
        booking_service(memory_store).create("T001", passengers(2))
    assert_domain_error(exc, "INSUFFICIENT_SEATS", 409)
    assert memory_store.trips["T001"].available_seats == 1
    assert memory_store.bookings == {}
    assert memory_store.orders == {}


def test_successful_mixed_booking_reserves_seats_and_starts_pending(memory_store):
    group = [Passenger("A", "Adult", PassengerType.ADULT), Passenger("S", "Student", PassengerType.STUDENT)]
    booking = booking_service(memory_store).create("T001", group)
    assert booking.status == BookingStatus.PENDING_PAYMENT
    assert booking.total_fare == 1225
    assert memory_store.trips["T001"].available_seats == 18
    assert memory_store.bookings[booking.booking_id] == booking
    assert memory_store.orders == {}


def test_missing_trip_rejected_without_mutating_store(memory_store):
    before = {key: trip.available_seats for key, trip in memory_store.trips.items()}
    with pytest.raises(DomainError) as exc:
        booking_service(memory_store).create("MISSING", passengers(1))
    assert_domain_error(exc, "TRIP_NOT_FOUND", 404)
    assert {key: trip.available_seats for key, trip in memory_store.trips.items()} == before
    assert memory_store.bookings == {}


def test_payment_success_marks_paid_and_creates_one_matching_order(memory_store):
    booking = booking_service(memory_store).create("T001", passengers(1))
    order = PaymentService(memory_store, MockPaymentGateway()).pay(booking.booking_id)
    assert booking.status == BookingStatus.PAID
    assert order.booking_id == booking.booking_id
    assert order.amount == booking.total_fare == 700
    assert order.payment_status == PaymentStatus.SUCCESS
    assert list(memory_store.orders.values()) == [order]
    assert OrderService(memory_store).get(order.order_id) == order
    assert memory_store.trips["T001"].available_seats == 19


def test_duplicate_payment_rejected_without_second_order(memory_store):
    booking = booking_service(memory_store).create("T001", passengers(1))
    service = PaymentService(memory_store, MockPaymentGateway())
    order = service.pay(booking.booking_id)
    with pytest.raises(DomainError) as exc:
        service.pay(booking.booking_id)
    assert_domain_error(exc, "BOOKING_NOT_PAYABLE", 409)
    assert booking.status == BookingStatus.PAID
    assert list(memory_store.orders.values()) == [order]
    assert memory_store.trips["T001"].available_seats == 19


def test_failed_payment_keeps_pending_without_order(memory_store):
    booking = booking_service(memory_store).create("T001", passengers(1))
    gateway = MockPaymentGateway()
    gateway.next_result = PaymentStatus.FAILED
    with pytest.raises(DomainError) as exc:
        PaymentService(memory_store, gateway).pay(booking.booking_id)
    assert_domain_error(exc, "PAYMENT_FAILED", 409)
    assert booking.status == BookingStatus.PENDING_PAYMENT
    assert memory_store.orders == {}
    assert memory_store.trips["T001"].available_seats == 19


def test_missing_booking_and_order_are_reported(memory_store):
    with pytest.raises(DomainError) as booking_exc:
        PaymentService(memory_store, MockPaymentGateway()).pay("MISSING")
    assert_domain_error(booking_exc, "BOOKING_NOT_FOUND", 404)
    with pytest.raises(DomainError) as order_exc:
        OrderService(memory_store).get("MISSING")
    assert_domain_error(order_exc, "ORDER_NOT_FOUND", 404)
    assert memory_store.bookings == {}
    assert memory_store.orders == {}
