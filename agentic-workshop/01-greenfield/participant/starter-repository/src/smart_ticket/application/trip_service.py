from smart_ticket.domain.models import Trip
from smart_ticket.infrastructure.store import InMemoryStore

class TripService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def query(self, origin: str | None = None, destination: str | None = None) -> list[Trip]:
        # TODO(GREENFIELD, TRIP-001, TRIP-002): Query sellable trips with optional filters.
        raise NotImplementedError("Trip query is not implemented in G0")
