from uuid import uuid4
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.models import BookingStatus, Order, PaymentStatus
from smart_ticket.infrastructure.store import InMemoryStore
from smart_ticket.infrastructure.payment_gateway import MockPaymentGateway
from smart_ticket.application.notification_service import NotificationService
from smart_ticket.application.audit_service import AuditService

class PaymentService:
    def __init__(self, store: InMemoryStore, gateway: MockPaymentGateway) -> None:
        self.store = store
        self.gateway = gateway
        self.notifications = NotificationService(store)
        self.audit = AuditService(store)

    def pay(self, booking_id: str) -> Order:
        with self.store.lock:
            booking = self.store.bookings.get(booking_id)
            if booking is None:
                raise DomainError("BOOKING_NOT_FOUND", "Booking not found", 404)
            if booking.status != BookingStatus.PENDING_PAYMENT:
                raise DomainError("BOOKING_NOT_PAYABLE", "Booking is not pending payment", 409)
            result = self.gateway.charge(booking_id, booking.total_fare)
            if result != PaymentStatus.SUCCESS:
                raise DomainError("PAYMENT_FAILED", "Payment failed", 409)
            order = Order(str(uuid4()), booking_id, booking.total_fare, result)
            self.store.orders[order.order_id] = order
            booking.status = BookingStatus.PAID
            self.audit.record(booking_id, "PAYMENT_COMPLETED")
            self.notifications.record(booking_id, "PAYMENT_COMPLETED")
            return order
