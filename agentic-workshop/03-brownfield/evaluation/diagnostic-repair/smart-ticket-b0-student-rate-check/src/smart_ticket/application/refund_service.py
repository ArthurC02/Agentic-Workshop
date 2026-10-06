from uuid import uuid4
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.models import BookingStatus
from smart_ticket.domain.records import RefundRecord
from smart_ticket.infrastructure.store import InMemoryStore
from smart_ticket.application.booking_service import BookingService
from smart_ticket.application.seat_service import SeatService
from smart_ticket.application.audit_service import AuditService
from smart_ticket.application.notification_service import NotificationService

class RefundService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store
        self.seats = SeatService(store)
        self.audit = AuditService(store)
        self.notifications = NotificationService(store)

    def refund(self, booking_id: str) -> RefundRecord:
        with self.store.lock:
            booking = BookingService(self.store, FarePolicy()).get(booking_id)
            if booking.status != BookingStatus.PAID or booking_id in self.store.refunds:
                raise DomainError("BOOKING_NOT_REFUNDABLE", "Only paid bookings can be refunded once", 409)
            record = RefundRecord(str(uuid4()), booking_id, booking.total_fare)
            self.seats.release(booking_id)
            booking.status = BookingStatus.REFUNDED
            booking.seat_ids = []
            self.store.refunds[booking_id] = record
            self.audit.record(booking_id, "BOOKING_REFUNDED")
            self.notifications.record(booking_id, "BOOKING_REFUNDED")
            return record
