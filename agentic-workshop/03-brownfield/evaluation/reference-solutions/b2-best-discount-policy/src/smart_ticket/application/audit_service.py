from uuid import uuid4
from smart_ticket.domain.errors import DomainError
from smart_ticket.domain.records import AuditEntry
from smart_ticket.infrastructure.store import InMemoryStore

class AuditService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def record(self, booking_id: str, event: str, detail: str = "") -> AuditEntry:
        entry = AuditEntry(str(uuid4()), booking_id, event, self.store.clock.now(), detail)
        self.store.audit_log.append(entry)
        return entry

    def list_for(self, booking_id: str) -> list[AuditEntry]:
        if booking_id not in self.store.bookings:
            raise DomainError("BOOKING_NOT_FOUND", "Booking not found", 404)
        return [entry for entry in self.store.audit_log if entry.booking_id == booking_id]
