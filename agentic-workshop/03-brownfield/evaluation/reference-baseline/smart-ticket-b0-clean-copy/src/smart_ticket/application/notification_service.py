from uuid import uuid4
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.records import NotificationRecord
from smart_ticket.infrastructure.store import InMemoryStore

class NotificationService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def record(self, booking_id: str, event: str) -> NotificationRecord:
        entry = NotificationRecord(str(uuid4()), booking_id, event, self.store.clock.now())
        self.store.notifications.append(entry)
        return entry

    def list_for(self, booking_id: str) -> list[NotificationRecord]:
        if booking_id not in self.store.bookings:
            raise DomainError("BOOKING_NOT_FOUND", "Booking not found", 404)
        return [entry for entry in self.store.notifications if entry.booking_id == booking_id]
