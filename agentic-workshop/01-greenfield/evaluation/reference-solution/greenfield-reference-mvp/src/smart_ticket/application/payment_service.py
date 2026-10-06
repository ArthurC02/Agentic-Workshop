from uuid import uuid4
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.models import BookingStatus, Order, PaymentStatus
from smart_ticket.domain.repositories import TicketRepositories
from smart_ticket.infrastructure.payment_gateway import MockPaymentGateway

class PaymentService:
    def __init__(self, store: TicketRepositories, gateway: MockPaymentGateway) -> None:
        self.store = store
        self.gateway = gateway

    def pay(self, booking_id: str) -> Order:
        with self.store.lock:
            booking = self.store.bookings.get(booking_id)
            if booking is None:
                raise DomainError("BOOKING_NOT_FOUND", "Booking not found", 404)
            # PAYMENT-001, PAYMENT-003: prevents repeated payment and duplicate orders.
            if booking.status != BookingStatus.PENDING_PAYMENT:
                raise DomainError("BOOKING_NOT_PAYABLE", "Booking is not pending payment", 409)
            result = self.gateway.charge(booking_id, booking.total_fare)
            if result != PaymentStatus.SUCCESS:
                # Failure preserves pending state, existing reservation, and no Order.
                raise DomainError("PAYMENT_FAILED", "Payment failed", 409)
            # PAYMENT-002, ORDER-001, ORDER-002: unique order and matching amount.
            order = Order(str(uuid4()), booking_id, booking.total_fare, result)
            self.store.orders[order.order_id] = order
            booking.status = BookingStatus.PAID
            return order
