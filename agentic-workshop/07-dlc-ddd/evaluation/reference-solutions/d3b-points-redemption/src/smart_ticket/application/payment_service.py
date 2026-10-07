from uuid import uuid4
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.models import BookingStatus, Order, PaymentStatus
from smart_ticket.infrastructure.store import InMemoryStore
from smart_ticket.infrastructure.payment_gateway import MockPaymentGateway
from smart_ticket.application.notification_service import NotificationService
from smart_ticket.application.audit_service import AuditService
from smart_ticket.application.seat_service import SeatService
from smart_ticket.application.member_service import MemberService
from smart_ticket.application.invoicing_service import InvoicingService
from smart_ticket.domain.invoicing import InvoiceBuyer

class PaymentService:
    def __init__(self, store: InMemoryStore, gateway: MockPaymentGateway,
                 invoicing: InvoicingService) -> None:
        self.store = store
        self.gateway = gateway
        self.invoicing = invoicing
        self.notifications = NotificationService(store)
        self.audit = AuditService(store)
        self.seats = SeatService(store)
        self.members = MemberService(store)

    def pay(self, booking_id: str, buyer: InvoiceBuyer = InvoiceBuyer()) -> Order:
        order = self._charge(booking_id, buyer)
        # EINV-002: the Order is committed before the provider is called, and issuing
        # reports failures as invoice state, so payment success is never rolled back.
        self.invoicing.issue(order.order_id)
        return order

    def _charge(self, booking_id: str, buyer: InvoiceBuyer) -> Order:
        with self.store.lock:
            booking = self.store.bookings.get(booking_id)
            if booking is None:
                raise DomainError("BOOKING_NOT_FOUND", "Booking not found", 404)
            if booking.status != BookingStatus.PENDING_PAYMENT:
                raise DomainError("BOOKING_NOT_PAYABLE", "Booking is not pending payment", 409)
            result = self.gateway.charge(booking_id, booking.payable_amount)
            if result != PaymentStatus.SUCCESS:
                if booking.booking_type == "GROUP":
                    self.seats.release(booking_id)
                    booking.status = BookingStatus.CANCELLED
                    booking.seat_ids = []
                    booking.assigned_seats = []
                    self.audit.record(booking_id, "GROUP_PAYMENT_FAILED")
                    self.members.restore_points(booking)
                    self.notifications.record(booking_id, "GROUP_BOOKING_CANCELLED")
                # PTS-011: an individual booking stays PENDING_PAYMENT and keeps its points.
                raise DomainError("PAYMENT_FAILED", "Payment failed", 409)
            order = Order(str(uuid4()), booking_id, booking.payable_amount, result)
            self.store.orders[order.order_id] = order
            booking.status = BookingStatus.PAID
            event = "GROUP_PAYMENT_COMPLETED" if booking.booking_type == "GROUP" else "PAYMENT_COMPLETED"
            self.audit.record(booking_id, event)
            self.notifications.record(booking_id, event)
            self.invoicing.open(order, booking, self.store.trips[booking.trip_id], buyer)
            return order

    def pay_group(self, booking_id: str, buyer: InvoiceBuyer = InvoiceBuyer()) -> Order:
        with self.store.lock:
            booking = self.store.bookings.get(booking_id)
            if booking is None:
                raise DomainError("BOOKING_NOT_FOUND", "Booking not found", 404)
            if booking.booking_type != "GROUP":
                raise DomainError("BOOKING_NOT_GROUP", "Booking is not a group booking", 409)
        # Released before pay(): pay() calls the invoice provider, which must not run under the lock.
        return self.pay(booking_id, buyer)
