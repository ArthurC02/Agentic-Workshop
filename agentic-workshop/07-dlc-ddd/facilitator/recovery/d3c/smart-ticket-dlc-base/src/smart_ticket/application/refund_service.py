from uuid import uuid4
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.fare_policy import FarePolicy
from smart_ticket.domain.records import RefundRecord
from smart_ticket.infrastructure.store import InMemoryStore
from smart_ticket.application.booking_service import BookingService
from smart_ticket.application.seat_service import SeatService
from smart_ticket.application.member_service import MemberService
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
            passenger_ids = booking.refund_in_full()
            # PTS-012: cash back is what was charged; the redeemed points go back as points.
            paid = next(order for order in self.store.orders.values() if order.booking_id == booking_id)
            record = RefundRecord(str(uuid4()), booking_id, paid.amount, passenger_ids, 0, self.store.clock.now())
            MemberService(self.store).restore_points(booking)
            self.seats.release(booking_id)
            self.store.refunds.append(record)
            self.audit.record(booking_id, "BOOKING_REFUNDED")
            self.notifications.record(booking_id, "BOOKING_REFUNDED")
            return record

    def cancel_passengers(self, booking_id: str, passenger_ids: list[str]) -> RefundRecord:
        """PCR-006, PCR-007, PCR-013, PCR-014. The Booking decides and refuses before anything changes;
        this applies its decision to the seat inventory and the refund ledger under the same lock.
        No gateway call: like the whole refund, only a local record (PCR-014)."""
        with self.store.lock:
            booking = BookingService(self.store, FarePolicy()).get(booking_id)
            departure = self.store.trips[booking.trip_id].departure_time.date()   # Taiwan date (+08:00)
            cancellation = booking.cancel_passengers(passenger_ids, (departure - self.store.clock.today).days)
            self.seats.release_passengers(booking_id, booking.trip_id, cancellation.passenger_ids)
            record = RefundRecord(str(uuid4()), booking_id, cancellation.refund, cancellation.passenger_ids,
                                  cancellation.fee, self.store.clock.now())
            self.store.refunds.append(record)
            self.audit.record(booking_id, "PASSENGERS_CANCELLED",
                              f"passenger_ids={','.join(record.passenger_ids)} refund={record.amount} fee={record.fee}")
            self.notifications.record(booking_id, "PASSENGERS_CANCELLED")
            return record

    def list_for(self, booking_id: str) -> list[RefundRecord]:
        """PCR-010: every refund of the booking, oldest first."""
        if booking_id not in self.store.bookings:
            raise DomainError("BOOKING_NOT_FOUND", "Booking not found", 404)
        return [record for record in self.store.refunds if record.booking_id == booking_id]
