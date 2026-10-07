from threading import RLock
from smart_ticket.domain.models import Booking, Order, Trip
from smart_ticket.domain.members import Member, MemberType
from smart_ticket.domain.invoicing import Invoice
from smart_ticket.domain.records import AuditEntry, NotificationRecord, RefundRecord, SeatAssignment
from smart_ticket.infrastructure.seed_data import build_seed_trips
from smart_ticket.infrastructure.clock import FixedClock

class InMemoryStore:
    def __init__(self) -> None:
        self.lock = RLock()
        self.clock = FixedClock()
        self.reset()

    def reset(self) -> None:
        with self.lock:
            self.clock.reset()
            self.trips: dict[str, Trip] = build_seed_trips()
            self.bookings: dict[str, Booking] = {}
            self.orders: dict[str, Order] = {}
            self.members = {mid: Member(mid, kind, points) for mid, kind, points in [
                ("M001", MemberType.STANDARD, 1200), ("M002", MemberType.CORPORATE, 5000),
                ("M003", MemberType.STANDARD, 0)]}
            self.seat_assignments: dict[str, list[SeatAssignment]] = {}
            self.refunds: dict[str, RefundRecord] = {}
            self.notifications: list[NotificationRecord] = []
            self.audit_log: list[AuditEntry] = []
            self.invoices: dict[str, Invoice] = {}   # keyed by order_id
            self.seat_capacity = {tid: trip.available_seats for tid, trip in self.trips.items()}
